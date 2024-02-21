#!/usr/bin/python3

from .user import User, Products, db

from .user import User, Products, db

def get_user_data(username):
    # Query the User table to get user information
    user = User.query.filter_by(username=username).first()

    if user is not None:
        return user
    else:
        # Handle the case where the user with the provided username is not found
        return None

