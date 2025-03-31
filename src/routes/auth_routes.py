from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.auth import create_user, set_user_password, authenticate_user, is_username_taken, is_email_taken
from utils.validators import validate_registration_form, validate_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Validate form data
        validation_errors = validate_registration_form(username, email, first_name, last_name, phone)
        
        if validation_errors:
            for error in validation_errors:
                flash(error, 'error')
            return render_template('create_account.html')
        
        # Check if username or email already exists
        if is_username_taken(username):
            flash('Username already taken', 'error')
            return render_template('create_account.html')
        
        if is_email_taken(email):
            flash('Email already registered', 'error')
            return render_template('create_account.html')
        
        # Create user without password
        user = create_user(username, email, first_name, last_name, phone)
        
        # Store user ID in session for password setting
        session['temp_user_id'] = user.id
        
        # Redirect to set password page
        return redirect(url_for('auth.set_password'))
    
    # GET request - show registration form
    return render_template('create_account.html')

@auth_bp.route('/set-password', methods=['GET', 'POST'])
def set_password():
    # Check if user is in the registration flow
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate password
        password_errors = validate_password(password, confirm_password)
        
        if password_errors:
            for error in password_errors:
                flash(error, 'error')
            return render_template('login_window.html')
        
        # Set user password
        user_id = session['temp_user_id']
        if set_user_password(user_id, password):
            # Clear temporary session data
            session.pop('temp_user_id', None)
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    
    # GET request - show set password form
    return render_template('login_window.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = authenticate_user(username, password)
        
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login_window.html', login_page=True)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))