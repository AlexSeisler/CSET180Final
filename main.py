import os
import random
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, or_
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='ecommerce'
    )

# Import Blueprints
from app.admin import admin
from app.vendor import vendor
from app.customer import customer
from app.auth import auth

# Load environment variables
load_dotenv()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    vendor = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(255))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer)  # optional, can be NULL for now
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    shipping_method = db.Column(db.String(50), nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    apt_suite = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_app():
    app = Flask(__name__)
    app.secret_key = '012345'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/ecommerce"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Setup MySQL connection
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    conn_str = f"mysql+pymysql://root:root@localhost/ecommerce"
    engine = create_engine(conn_str, echo=True)
    app.config['ENGINE'] = engine

    # Register Blueprints
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(vendor, url_prefix='/vendor')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(auth, url_prefix='/auth')

    # Default route
    @app.route('/')
    def index():
        all_products = Product.query.all()
        featured = random.sample(all_products, min(len(all_products), 4))
        return render_template('home.html', featured=featured)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            if User.query.filter_by(username=username).first():
                flash('Username already exists.')
                return redirect(url_for('register'))

            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('index'))

        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.')
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            login_id = request.form['login_id']
            password = request.form['password']

            user = User.query.filter(
                or_(User.username == login_id, User.email == login_id)
            ).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect(url_for('index'))
            else:
                flash('Invalid login credentials.')

        return render_template('login.html')

    from sqlalchemy import or_

    @app.route("/search", methods=["GET"])
    def search():
        query = request.args.get("q", "")
        department = request.args.get("department", "")
        name = request.args.get("name", "")
        description = request.args.get("description", "")
        vendor = request.args.get("vendor", "")
        size = request.args.get("size", "")
        color = request.args.get("color", "")
        availability = request.args.get("availability", "")
        sort = request.args.get("sort", "")

        results = Product.query

        if query:
            results = results.filter(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                    Product.vendor.ilike(f"%{query}%")
                )
            )
        if name:
            results = results.filter(Product.name.ilike(f"%{name}%"))
        if description:
            results = results.filter(Product.description.ilike(f"%{description}%"))
        if vendor:
            results = results.filter(Product.vendor.ilike(f"%{vendor}%"))
        if availability == "In Stock":
            results = results.filter(Product.price > 0)  # adjust if you have a stock column
        elif availability == "Out of Stock":
            results = results.filter(Product.price == 0)


        if sort == "price_asc":
            results = results.order_by(Product.price.asc())
        elif sort == "price_desc":
            results = results.order_by(Product.price.desc())
        elif sort == "name_asc":
            results = results.order_by(Product.name.asc())

        products = results.all()

        return render_template("search.html", products=products, search=query, department=department, request=request)

    @app.route('/product/<int:product_id>', methods=['GET', 'POST'])
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            comment = request.form['comment']
            rating = int(request.form['rating'])

            new_review = Review(product_id=product.id, comment=comment, rating=rating)
            db.session.add(new_review)
            db.session.commit()
            return redirect(url_for('product_detail', product_id=product_id))

        reviews = Review.query.filter_by(product_id=product_id).all()
        return render_template('product.html', product=product, reviews=reviews)

    @app.route('/product/<int:product_id>/review', methods=['GET', 'POST'])
    def write_review(product_id):
        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            comment = request.form['comment']
            rating = int(request.form['rating'])

            new_review = Review(product_id=product.id, comment=comment, rating=rating)
            db.session.add(new_review)
            db.session.commit()
            return redirect(url_for('product_detail', product_id=product.id))

        return render_template('write_review.html', product=product)

    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        product = Product.query.get_or_404(product_id)

        cart = session.get('cart', [])

        product_in_cart = next((item for item in cart if item['id'] == product.id), None)

        if product_in_cart:

            product_in_cart['quantity'] += 1
        else:
            cart.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image_url,
                'quantity': 1
            })

        session['cart'] = cart
        flash('Added to cart!')
        return redirect(url_for('cart'))

    @app.route('/cart')
    def cart():
        cart = session.get('cart', [])
        total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart)

        recommended = [
            {'id': 101, 'image_url': 'https://via.placeholder.com/300x200?text=Rec1'},
            {'id': 102, 'image_url': 'https://via.placeholder.com/300x200?text=Rec2'},
            {'id': 103, 'image_url': 'https://via.placeholder.com/300x200?text=Rec3'},
        ]

        return render_template('cart.html', cart=cart, total=total, recommended=recommended)

    @app.route('/update_cart', methods=['POST'])
    def update_cart():
        quantities = request.form.to_dict(flat=False)
        cart = session.get('cart', [])

        for key, value_list in quantities.items():
            if key.startswith('quantities['):
                try:
                    product_id = int(key[len('quantities['):-1])
                    quantity = int(value_list[0])

                    for item in cart:
                        if item['id'] == product_id:
                            item['quantity'] = quantity
                except ValueError:
                    continue

        remove_id = request.form.get('remove_id')
        if remove_id:
            cart = [item for item in cart if item['id'] != int(remove_id)]

        session['cart'] = cart
        session.modified = True
        return redirect(url_for('cart'))

    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        cart = session.get('cart', [])
        total = sum(item['price'] for item in cart)
        return render_template('checkout.html', cart=cart, total=total)

    @app.route('/place_order', methods=['POST'])
    def place_order():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        cart = session.get('cart', [])
        total = 0.0

        for item in cart:
            product = Product.query.get(item['id'])
            if product:
                total += product.price

        shipping_method = request.form['shipping_method']
        shipping_cost = 0.0
        if shipping_method == "Two day":
            shipping_cost = 5.0
        elif shipping_method == "One day":
            shipping_cost = 10.0

        total += shipping_cost

        new_order = Order(
            user_id=session['user_id'],
            total=total,
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            zip_code=request.form['zip_code'],
            apt_suite=request.form.get('apt', '')
        )

        db.session.add(new_order)
        db.session.commit()

        session.pop('cart', None)
        session.pop('cart_total', None)

        return redirect(url_for('order_confirmation', order_id=new_order.id))

    @app.route('/order/confirmation/<int:order_id>')
    def order_confirmation(order_id):
        order = Order.query.get_or_404(order_id)
        return render_template('confirmation.html', order=order)

    @app.route('/product/<int:product_id>/reviews')
    def view_reviews(product_id):
        sort = request.args.get('sort', 'desc')  # 'asc' or 'desc'
        keyword = request.args.get('keyword', '')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        query = "SELECT * FROM review WHERE product_id = %s"
        params = [product_id]

        if keyword:
            query += " AND (comment LIKE %s)"
            params.append(f"%{keyword}%")

        if sort == 'asc':
            query += " ORDER BY rating ASC"
        else:
            query += " ORDER BY rating DESC"

        cur.execute(query, params)
        reviews = cur.fetchall()
        conn.close()

        return render_template('reviews.html', reviews=reviews, product_id=product_id, sort=sort, keyword=keyword)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)









