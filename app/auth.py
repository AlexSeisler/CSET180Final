from flask import Blueprint
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from app.models import db


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return redirect(url_for('index'))

    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']

        user = User.query.filter(
            or_(User.username == login_id, User.email == login_id)
        ).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid login credentials.')

    return render_template('login.html')