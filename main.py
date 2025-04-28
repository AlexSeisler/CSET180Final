import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, or_
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

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
        return render_template('home.html')

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

    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        return render_template('product.html', product=product)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)







