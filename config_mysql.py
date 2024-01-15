#!/usr/bin/python3

import os
import mysql.connector
import getpass

# MySQL configurations
mysql_host = 'localhost'
mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_db = 'island'

# Prompt the user for the MySQL password
mysql_password = getpass.getpass("Enter MySQL password: ")

# Initialize MySQL connection
mysql_conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
        )

# Create a cursor object with dictionary=True
cursor = mysql_conn.cursor(dictionary=True)

# Now you can use the 'cursor' object to execute SQL queries

# For example:
cursor.execute("SELECT * FROM users")
result = cursor.fetchall()

# Don't forget to close the cursor and connection when done
cursor.close()
mysql_conn.close()

# You can use 'result' to retrieve data from the executed query
print(result)

