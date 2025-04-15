from src.models.user import User
from src.models.database import db, init_db
from flask import session
from werkzeug.security import generate_password_hash

app = Flask(__name__)
init_db(app)

def create_user(username, email, first_name, last_name, phone_number=None):
    """Create a new user witßhout password"""
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
        session['user_id'] = user.id
        return user
    return None

def logout_user():
    """Log out the current user"""
    session.pop('user_id', None)
    return True

def get_current_user():
    """Get current logged in user"""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def is_username_taken(username):
    """Check if username already exists"""
    return User.query.filter_by(username=username).first() is not None

def is_email_taken(email):
    """Check if email already exists"""
    return User.query.filter_by(email=email).first() is not None

def add_user(username, email, first_name, last_name, password, phone_number = None):
    """Add a new user to the database"""
    with app.app_context():
        # Check if username or email is already taken
        if is_username_taken(username):
            print(f"Error: Username '{username}' is already taken")
            return False
        
        if is_email_taken(email):
            print(f"Error: Email '{email}' is already in use")
            return False
        
        # Create the user
        user = create_user(username, email, first_name, last_name, phone_number)

        # Set password
        set_user_password(user.id, password)

        print(f"User '{username}' created successfully with ID: {user.id}")
        return True

def list_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("No users found in the database")
            return
        
        print(f"Total users: {len(users)}")
        print("-" * 80)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Name':<30}")
        print("-" * 80)

        for user in users:
            name = f"{user.first_name} {user.last_name}"
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {name:<30}")

def find_user(identifier):
    """Find a user by username, email, or ID"""
    with app.app_context():
        # Try to find by ID
        if identifier.isdigit():
            user = User.query.get(int(identifier))
            if user: 
                return user
    
        # Try to find by username
        user = User.query.filter_by(username = identifier).first()
        if user:
            return user
            
        # Try to find by email
        user = User.query.filter_by(email = identifier).first()
        if user:
            return user

        return None
    
def show_user_details(identifier):
    """Show detailed information about a user"""
    with app.app_context():
        user = find_user(identifier)
        if not user:
            print(f"User not found: {identifier}")
            return False
        
        print("-" * 50)
        print(f"User Details - ID: {user.id}")
        print("-" * 50)
        print(f"Username:     {user.username}")
        print(f"Email:        {user.email}")
        print(f"Name:         {user.first_name} {user.last_name}")
        print(f"Phone:        {user.phone_number or 'Not provided'}")
        print(f"Created at:   {user.created_at}")
        print(f"Last updated: {user.updated_at}")
        print("-" * 50)
        return True
    
def update_user_password(identifier, new_password):
    """Update a user's password"""
    with app.app_context():
        user = find_user(identifier)
        if not user:
            print(f"User not found: {identifier}")
            return False
    
        user.set_password(new_password)
        from src.models.database import db 
        db.session.commit()
        print(f"Password updated for user: {user.username}")
        return True
