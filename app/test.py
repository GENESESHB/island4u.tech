#!/usr/bin/python3
"""starting flask"""

import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'island'
}
#establish a connection to mysql
connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="island"
)
#stor all email in var
cursor = connection.cursor()
cursor.execute("SELECT GROUP_CONCAT(email SEPARATOR ',') FROM users")
result1 = cursor.fetchone()
email_list = result1[0] if result1 else None

cursor.execute("SELECT GROUP_CONCAT(password SEPARATOR ',') FROM users")
result2 = cursor.fetchone()
password_list = result2[0] if result2 else None

# path to mester json
json_file_path = os.path.join(os.path.dirname(__file__), 'register_data.json')

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Call the user_existe function
    user_exists_result = user_existe(email, password)

    if user_exists_result == 'exists':
        return 'User already exists!'
    else:
        # Create a dictionary for mister json
        registration_data = {
            'username' : username,
            'email' : email,
            'password' : password
        }

        # Save the register_data in mester json
        with open(json_file_path, 'a') as json_file:
            json.dump(registration_data, json_file)
            json_file.write('\n')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            conn.commit()
            return 'Registration successful!'
        except Exception as e:
            conn.rollback()
            return f'Error: {e}'
        finally:
            cursor.close()
            conn.close()

def user_existe(email, password):
    if email in email_list and password in password_list:
        return 'exists'
    else:
        return 'not exists'

if __name__ == '__main__':
    app.run(debug=True)

