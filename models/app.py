#!/usr/bin/python3
"""starting flask"""

from flask_migrate import Migrate
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .user import User, Products, db  # Import Product model
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import uuid

login_manager = LoginManager()
login_manager.login_view = 'login'
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imobi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'HASSANBOUDRAA8@'
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded images

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader function for Flask-Login
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
                flash(
    'Invalid email or password. Please try again or register.',
     'error')
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
        user_products = Products.query.filter_by(user_id=current_user.id).all()
        return render_template('user.html', user=current_user, products=user_products)

    @app.route('/exit')
    def exit():
        return render_template('login.html')

    @app.route('/products')
    @login_required
    def products():
        user_products = Products.query.filter_by(user_id=current_user.id).all()
        for product in user_products:
            print("Product Image Path:", product.image_path)
        return render_template('products.html', user=current_user, user_products=user_products)
    
    @app.route('/add_product', methods=['GET', 'POST'])
    @login_required
    def add_product():
        if request.method == 'POST':
            name = request.form['name']
            price = float(request.form['price'])
            image_path = save_uploaded_image(request.files['image'])
            user_id = current_user.id
            num_rooms = int(request.form['num_rooms'])
            num_salon = int(request.form['num_salon'])
            num_bain = int(request.form['num_bain'])
            window_per_chamber = int(request.form['window_per_chamber'])
            
            new_product = Products(
                    name=name, 
                    price=price, 
                    image_path=image_path, 
                    num_rooms=num_rooms, 
                    num_salon=num_salon, 
                    num_bain=num_bain, 
                    window_per_chamber=window_per_chamber, 
                    user=current_user)

            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully.', 'success')
            return redirect(url_for('products'))

        return render_template('add_product.html')
    
    def save_uploaded_image(file):
        if file:
            file_name = str(uuid.uuid4()) + file.filename
            file_path = os.path.join(app.root_path, 'uploads', file_name)
            file.save(file_path)
            return file_path
        return None
    
    @app.route('/all_products')
    @login_required
    def all_products():
        all_products = Products.query.all()
        
        processed_products = [
                {
                    'name': product.name,
                    'price': product.price,
                    'num_rooms': product.num_rooms,
                    'num_salon': product.num_salon,
                    'num_bain': product.num_bain,
                    'window_per_chamber': product.window_per_chamber,
                    'image_path': os.path.basename(product.image_path) if product.image_path else None,
                }
                    for product in all_products
        ]

        return render_template('all_products.html', all_products=processed_products)
    
    @app.route('/serve_image/<filename>', methods=['GET'])
    def serve_image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()

    return app

