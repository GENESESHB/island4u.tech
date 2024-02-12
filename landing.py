#!/usr/bin/python3
import os
from flask import render_template
from models import Products  # Assuming your Products model is in the user module

def landing():
    # Retrieve all products for display
    all_products = Products.query.all()

    # Process the product details for rendering
    processed_products = [
        {
            'name': product.name,
            'city': product.city,
            'price': product.price,
            'num_rooms': product.num_rooms,
            'section': product.section,
            'num_bain': product.num_bain,
            'window_per_house': product.window_per_house,
            'image_path': os.path.basename(product.image_path) if product.image_path else None,
            'product_id_string': str(product.id),
        }
        for product in all_products
    ]

    print("all_products")

