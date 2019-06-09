from flask import Flask, render_template, request, Blueprint, redirect, flash, url_for, session, g


from bokeh.embed import server_document, server_session

from bokeh.client import pull_session
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)
from forms import RegistrationForm, LoginForm

import subprocess
from werkzeug.contrib.fixers import ProxyFix



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


#changing the host
def bash_command(cmd):
    subprocess.Popen(cmd, shell=True)
bash_command('bokeh serve ./line.py --allow-websocket-origin=127.0.0.1:5000')

def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        g.dbConn = connect(connStr)
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')

@app.route("/")
@app.route("/welcome")
def main():
        return render_template('welcome.html', title='welcome')

@app.route("/home")
def home():
        return render_template('home.html')


@app.route("/about")
def about():
        return render_template('about.html', title='About')

#method list is to accept post requists
# calidate if this form have already submitted 
# flash kmessage is to one time alert, f for passing string

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT * FROM db_user WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO db_user (user_email, user_name, user_password) VALUES (%s, %s, %s)',
                (email, username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            return redirect(url_for('home'))

        flash(error)
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM db_user WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[3], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('home'))

        flash(error)
    if form.validate_on_submit():
        flash(f' {form.username.data} , you are successfully logged in!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


# @app.route("/statistics")
# def statistics():
#     script=server_document("http://localhost:5006/graphs")
#     print(script)
#     return render_template('statistics.html', bokS=script, title='Statistics')
app.wsgi_app=ProxyFix(app.wsgi_app)


@app.route("/statistics")
def statistics():
    script=server_document("http://localhost:5006/line")
    print(script)
    return render_template('statistics.html',bokS=script)


    # # pull a new session from a running Bokeh server
    # with pull_session(url="http://localhost:5006/graphs") as session:

    #     # # update or customize that session
    #     # session.document.roots[0].children[1].title.text = "graphplease"

    #     # generate a script to load the customized session
    #     script = server_session(session_id=session.id, url='http://localhost:5006/graphs')

    #     # use the script in the rendered page
    #     return render_template("statistics.html", script=script, template="Flask")




if __name__ == '__main__':
        app.run(debug=True, use_reloader=True)       



