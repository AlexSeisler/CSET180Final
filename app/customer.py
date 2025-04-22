from flask import Blueprint

customer = Blueprint('customer', __name__, url_prefix='/customer')

# Add routes for the customer blueprint
@customer.route('/')
def customer_home():
    return 'customer Home'