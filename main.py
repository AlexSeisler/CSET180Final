from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from flask import flash, redirect, url_for
from dotenv import load_dotenv

load_dotenv()  # Loads from .env

SMTP_SERVER = os.getenv('SMTP_SERVER')

app = Flask(__name__)


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
# DB connection
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fixed connection string with DB specified
conn_str = f"mysql+pymysql://root:{ADMIN_PASSWORD}@localhost/ecommerce"
engine = create_engine(conn_str, echo=True)

conn = engine.connect()

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

