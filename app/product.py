from flask import Blueprint, render_template

product = Blueprint('product', __name__, url_prefix='/product')

@product.route('/')
def product_home():
    return f'{product.name.capitalize()} Home Page'