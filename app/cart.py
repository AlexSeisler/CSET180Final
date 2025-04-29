from flask import Blueprint, render_template

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/')
def cart_home():
    return f'{cart.name.capitalize()} Home Page'