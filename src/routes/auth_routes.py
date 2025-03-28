from flask import Blueprint, render_template, request, redirect, url_for, session
from core.auth import authenticate_user, create_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticate_user(username, password):
            session['user'] = username
            return redirect(url_for('home'))
        # Handle authentication failure
    return render_template('login_window.html')

@bp.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Extract user data from form
        user_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'email': request.form.get('email')
        }
        create_user(user_data)
        return redirect(url_for('auth.login'))
    return render_template('create_account.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))