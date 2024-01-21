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
"""
cursor.execute("SELECT GROUP_CONCAT(password SEPARATOR ',') FROM users")
result2 = cursor.fetchone()
password_list = result2[0] if result2 else None
"""
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

    if email in email_list:
        return render_template('dashboard.html')
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
            return render_template('dashboard.html')
        except Exception as e:
            conn.rollback()
            return f'Error: {e}'
        finally:
            cursor.close()
            conn.close()


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/user')
def user():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)

