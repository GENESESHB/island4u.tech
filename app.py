from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'your_mysql_server',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'your_database_name'
}

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

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
