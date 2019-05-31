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
    
    
  
    postgres_insert_query = """ INSERT INTO db_user (user_id, user_email, user_name, user_password) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (1, 'dilara@trail.com', 'Dilara', 'rdz123')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into db_user table")
except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into db_user table", error)
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")