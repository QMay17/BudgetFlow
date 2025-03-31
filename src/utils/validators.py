import re

def validate_registration_form(username, email, first_name, last_name, phone=None):
    """Validate registration form data"""
    errors = []
    
    # Username validation
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters long")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        errors.append("Username can only contain letters, numbers, and underscores")
    
    # Email validation
    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append("Please enter a valid email address")
    
    # Name validation
    if not first_name:
        errors.append("First name is required")
    
    if not last_name:
        errors.append("Last name is required")
    
    # Phone validation (optional)
    if phone and not re.match(r'^\+?[0-9\-\s]{10,15}$', phone):
        errors.append("Please enter a valid phone number")
    
    return errors

def validate_password(password, confirm_password):
    """Validate password"""
    errors = []
    
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")
    
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    return errors