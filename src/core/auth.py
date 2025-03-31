from models.user import User
from models.database import db
from flask import session
from werkzeug.security import generate_password_hash

def create_user(username, email, first_name, last_name, phone_number=None):
    """Create a new user without password"""
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )
    
    db.session.add(user)
    db.session.commit()
    return user

def set_user_password(user_id, password):
    """Set password for a user"""
    user = User.query.get(user_id)
    if user:
        user.set_password(password)
        db.session.commit()
        return True
    return False

def authenticate_user(username, password):
    """Authenticate a user with username and password"""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def is_username_taken(username):
    """Check if username already exists"""
    return User.query.filter_by(username=username).first() is not None

def is_email_taken(email):
    """Check if email already exists"""
    return User.query.filter_by(email=email).first() is not None