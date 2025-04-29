from flask import Blueprint, render_template

review = Blueprint('review', __name__, url_prefix='/review')

@review.route('/')
def review_home():
    return f'{review.name.capitalize()} Home Page'