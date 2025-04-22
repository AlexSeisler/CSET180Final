import os
from flask import Flask, render_template
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Import Blueprints
from app.admin import admin
from app.vendor import vendor
from app.customer import customer
from app.auth import auth

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a secure key for production

    # Setup MySQL connection
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    conn_str = f"mysql+pymysql://root:{ADMIN_PASSWORD}@localhost/ecommerce"
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
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)



