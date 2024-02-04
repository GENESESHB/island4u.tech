#!/usr/bin/python3
"""starting flask"""

from flask_migrate import Migrate
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'login'
migrate = Migrate()

# User class for Flask-Login
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

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'HASSANBOUDRAA8@'

    db.init_app(app)
    migrate.init_app(app, db)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            city = request.form['city']
            email = request.form['email']
            password = request.form['password']

            new_user = User(username=username, city=city, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again or register.', 'error')
                return redirect(url_for('signup'))

        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', user=current_user)

    @app.route('/user')
    @login_required
    def user():
        user_id = current_user.id
        username = current_user.username
        email = current_user.email
        return render_template('user.html', username=username, email=email, user_id=user_id)
    
    @app.route('/exit')
    def exit():
        return render_template('login.html')
    
    with app.app_context():
        db.create_all()

    return app

