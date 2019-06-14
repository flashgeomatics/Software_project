#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "ruking29",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "se4g")
    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE db_user
          (user_id SERIAL PRIMARY KEY,
            user_email VARCHAR(255) UNIQUE NOT NULL,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            user_password VARCHAR(255) NOT NULL); '''
    
    cursor.execute(create_table_query) 
    connection.commit()
    print("Table created successfully in PostgreSQL ")
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)

  
    
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")