#!/usr/bin/python3
"""
class user for stor data info and sqlalchemy
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(28), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    product_name = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='products')

    def __init__(self, product_name, price, user):
        self.product_name = product_name
        self.price = price
        self.user = user
