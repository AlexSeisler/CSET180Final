from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Add routes for the Auth blueprint
@auth.route('/')
def auth_home():
    return 'Auth Home'