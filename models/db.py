#!/usr/bin/python3

from .user import User, Products, db

def get_user_data(username):
    # Step 1: Query the User table to get user information
    user = User.query.filter_by(username=username).first()

    if user is not None:
        # Step 2: Query the Products table to get user's products
        user_products = Products.query.filter_by(user_id=user.id).all()

        # Step 3: Format the data as needed
        formatted_user_data = {
            'username': user.username,
            'city': user.city,
            'email': user.email,
            'products': [{'name': product.name, 'price': product.price} for product in user_products]
            # Add more fields as needed
        }

        return formatted_user_data
    else:
        # Handle the case where the user with the provided username is not found
        return None

