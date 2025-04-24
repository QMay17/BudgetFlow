from src.models.user import User
from tkinter import messagebox

class AuthManager:
    """Manages user authentication and registration."""
    
    def __init__(self):
        self.current_user = None
    
    def register_user(self, username, email, full_name, password, confirm_password):
        """Register a new user."""

        # Input validation
        if not username or not email or not full_name or not password:
            return False, "All fields are required"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if username or email already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            return False, "username_exists"
        
        existing_email = User.find_by_email(email)
        if existing_email:
            return False, "email_exists"
        
        try:
            # Create new user
            user = User.create(username, email, full_name, password)
            print(f"[DEBUG] User successfully registered: {user}")
            self.current_user = user
            return True, "Registration successful"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username, password):
        """Login a user with username and password."""

        user = User.find_by_username(username)
        if not user:
            return False, "Invalid username or password"
        
        if not User.verify_password(user.password_hash, password):
            return False, "Invalid username or password"

        self.current_user = user
        return True, "Login successful"

    
    def logout(self):
        """Log out the current user."""
        self.current_user = None
        return True
    
    def is_logged_in(self):
        """Check if a user is logged in."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get the currently logged in user."""
        return self.current_user