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

# Path to master json
json_file_path = os.path.join(os.path.dirname(__file__), 'register_data.json')

# Check if user exists
def user_exists(email, password):
    with open(json_file_path, 'r') as json_file:
        for line in json_file:
            try:
                user_data = json.loads(line)
                if user_data['email'] == email and check_password_hash(user_data['password'], password):
                    return True
            except json.decoder.JSONDecodeError:
                pass
    return False

# Write to JSON file only if user doesn't exist
def write_to_json(data):
    if not user_exists(data['email'], data['password']):
        with open(json_file_path, 'a') as json_file:
            json.dump(data, json_file)
            json_file.write('\n')

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if user_exists(email, password):
        return render_template('index.html')

    # Create a dictionary for master json
    registration_data = {
        'username': username,
        'email': email,
        'password': password
    }

    # Save the registration_data in master json only if the user doesn't exist
    write_to_json(registration_data)

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

