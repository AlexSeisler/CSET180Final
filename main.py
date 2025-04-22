from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from flask import flash, redirect, url_for
from dotenv import load_dotenv

load_dotenv()  # Loads from .env
app = Flask(__name__)


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
# DB connection
app = Flask(__name__)
app.secret_key = 'your_secret_key'

#To access your own local database though your dev/feature branch, you need to set up a .env file with the following variables:
# ADMIN_USERNAME=your_username
# ADMIN_PASSWORD=your_password
conn_str = f"mysql+pymysql://root:{ADMIN_PASSWORD}@localhost/ecommerce"
engine = create_engine(conn_str, echo=True)

conn = engine.connect()

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

