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

    #create a dictionary for mister json
    registration_data = {
            'username' : username,
            'email' : email,
            'password' : password
            }

    #save the register_data in mester json
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

if __name__ == '__main__':
    app.run(debug=True)
