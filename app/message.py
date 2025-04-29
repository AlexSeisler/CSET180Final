from flask import Blueprint, render_template

message = Blueprint('message', __name__, url_prefix='/message')

@message.route('/')
def message_home():
    return f'{message.name.capitalize()} Home Page'