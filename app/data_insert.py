#!/usr/bin/python3

import mysql.connector

def insert_user_data(user_data):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="island"
        )

        cursor = connection.cursor()

        # Insert data into the 'users' table
        insert_query = "INSERT INTO users (name, email, password, username) VALUES (%s, %s, %s, %s)"
        insert_data = (user_data['name'], user_data['email'], user_data['password'], user_data['username'])

        cursor.execute(insert_query, insert_data)

        # Commit the changes
        connection.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    # Example data to insert
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'secure_password',
        'username': 'john_doe'
    }

    # Insert data
    insert_user_data(user_data)
