#!/usr/bin/python3
"""
class user for stor data info and sqlalchemy
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, desc
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True, default=lambda: str( uuid.uuid4()), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(28), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Products(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=lambda: str( uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(8), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    num_rooms = Column(Integer, nullable=False)
    section = Column(Integer, nullable=False)
    num_bain = Column(Integer, nullable=False)
    window_per_house = Column(Integer, nullable=False)
    user_id = db.Column(db.String(50),db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))

class Iprofile(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=lambda: str( uuid.uuid4()), unique=True, nullable=False)
    imageprofile_path = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.String(50),db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('Iprofile', lazy=True))

class Icover(db.Model):
     id = db.Column(db.String(50), primary_key=True, default=lambda: str( uuid.uuid4()), unique=True, nullable=False)
     imagecover_path = db.Column(db.String(255), nullable=True)
     user_id = db.Column(db.String(50),db.ForeignKey('user.id'),nullable=False)
     user = db.relationship('User', backref=db.backref('Icover', lazy=True))

