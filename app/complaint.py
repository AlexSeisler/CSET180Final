from flask import Blueprint, render_template

complaint = Blueprint('complaint', __name__, url_prefix='/complaint')

@complaint.route('/')
def complaint_home():
    return f'{complaint.name.capitalize()} Home Page'