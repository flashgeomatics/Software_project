from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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



if __name__ == '__main__':
        app.run(debug=True, use_reloader=True)        

