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

# path to master json
json_file_path = os.path.join(os.path.dirname(__file__), 'register_data.json')

# Function to check if user exists
def user_exists(email, password):
    # Check in the JSON file
    with open(json_file_path, 'r') as json_file:
        for line in json_file:
            try:
                user_data = json.loads(line)
                if user_data['email'] == email and check_password_hash(user_data['password'], password):
                    return True
            except json.decoder.JSONDecodeError:
                pass
    
    # Check in the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result and check_password_hash(result[2], password):
            return True
    except Exception as e:
        print(f'Error checking user in database: {e}')
    finally:
        cursor.close()
        conn.close()

    return False

# Route for the home page
@app.route('/')
def index():
    return render_template('register.html')

# Route for handling registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Check if user exists in the database or JSON file
    if user_exists(email, password):
        return render_template('index.html')

    # If the user doesn't exist, proceed with registration

    # Save the registration data in the master JSON file
    registration_data = {
        'username': username,
        'email': email,
        'password': password
    }

    with open(json_file_path, 'a') as json_file:
        json.dump(registration_data, json_file)
        json_file.write('\n')

    # Insert the user into the database
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

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

