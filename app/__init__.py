from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define db here, at the top

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/ecommerce"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = '012345'

    db.init_app(app)

    # Import models AFTER db is initialized to avoid circular import
    from app import models

    # Register Blueprints AFTER models
    from app.admin import admin
    from app.vendor import vendor
    from app.customer import customer
    from app.auth import auth
    from app.product import product
    from app.order import order
    from app.cart import cart
    from app.review import review
    from app.complaint import complaint
    from app.message import message
    from app.home import home

    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(vendor, url_prefix='/vendor')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(product, url_prefix='/product')
    app.register_blueprint(order, url_prefix='/order')
    app.register_blueprint(cart, url_prefix='/cart')
    app.register_blueprint(review, url_prefix='/review')
    app.register_blueprint(complaint, url_prefix='/complaint')
    app.register_blueprint(message, url_prefix='/message')
    app.register_blueprint(home, url_prefix='/home')

    return app


    """
    #Need to find a home for these...
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
            results = results.filter(Product.price > 0)
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
    """
    
