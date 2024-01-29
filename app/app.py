#!/usr/bin/python3
"""starting flask"""

import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid
import json
from models.user import User
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
        # Create a User instance
        user = User(username, email, password)

        # Create a dictionary for mister json
        registration_data = {
            'user_id': user.user_id,
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
            cursor.execute("INSERT INTO users (user_id, username, email, password) VALUES (%s, %s, %s, %s)", (user.user_id, username, email, hashed_password))
            conn.commit()
            return render_template('dashboard.html')
        except Exception as e:
            conn.rollback()
            return f'Error: {e}'
        finally:
            cursor.close()
            conn.close()

#login_flask
login_manager = LoginManager(app)
login_manager.login_view = 'register'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            user_id, username, email, hashed_password = user_data
            return User(user_id, username, email, hashed_password)
        else:
            return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/user')
def user():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        # Use current_user to access the logged-in user's information
        user_id = current_user.id
        username = current_user.username
        email = current_user.email
        return render_template('user.html', user_id=user_id, username=username, email=email)
    else:
        return render_template('user.html', user_id=None, username=None, email=None)


@app.route('/sign')
def sign():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

