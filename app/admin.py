from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Add routes for the admin blueprint
@admin.route('/')
def admin_home():
    return 'Admin Home'