from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import random
from datetime import datetime
from flask import jsonify
from flask_mail import Mail, Message
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from flask import flash, redirect, url_for

load_dotenv()  # Loads from .env

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))

ADMIN_USERNAME = 'AlexSeisler'
ADMIN_PASSWORD = 'Lightweight82806!'

app = Flask(__name__)

# DB connection
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fixed connection string with DB specified
conn_str = "mysql+pymysql://root:Lightweight82806!@localhost/bank_app"
engine = create_engine(conn_str, echo=True)

conn = engine.connect()

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

