from flask import Blueprint

vendor = Blueprint('vendor', __name__, url_prefix='/vendor')

# Add routes for the vendor blueprint
@vendor.route('/')
def vendor_home():
    return 'vendor Home'