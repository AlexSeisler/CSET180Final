from flask import Blueprint, render_template

order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/')
def order_home():
    return f'{order.name.capitalize()} Home Page'