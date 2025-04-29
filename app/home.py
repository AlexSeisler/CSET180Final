from flask import Blueprint, render_template

# Define the blueprint for 'home' with the URL prefix '/home'
home = Blueprint('home', __name__, url_prefix='/home')

# Route to render the home.html template
@home.route('/')
def home_home():
    return render_template('home.html')