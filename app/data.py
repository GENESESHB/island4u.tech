#!/usr/bin/python3

"""ng flask"""

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

print (password_list)
print(email_list)
