from src.core.auth import AuthManager
from tkinter import messagebox

class AuthController:
    """Controller class to handle authentication logic."""
    
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.auth_manager = AuthManager()
    
    def handle_registration(self, username, email, full_name, password, confirm_password):
        """Handle user registration."""
        success, message = self.auth_manager.register_user(
            username, email, full_name, password, confirm_password
        )
        
        if success:
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.app_controller.show_frame("login")
            return True
        else:
            # Check if it's a unique constraint error
            if message == "username_exists":
                response = messagebox.askquestion(
                    "Username Exists", 
                    "This username is already in use. Would you like to log in instead?",
                    icon='question'
                )
                if response == 'yes':
                    self.app_controller.show_frame("login")
                return False
            elif message == "email_exists":
                response = messagebox.askquestion(
                    "Email Exists", 
                    "This email is already registered. Would you like to log in instead?",
                    icon='question'
                )
                if response == 'yes':
                    self.app_controller.show_frame("login")
                return False
            else:
                messagebox.showerror("Registration Error", message)
                return False
    
    def handle_login(self, username, password):
        """Handle user login."""
        success, message = self.auth_manager.login(username, password)
        
        if success:
            # Notify that auth state changed
            if hasattr(self, 'on_auth_changed') and self.on_auth_changed:
                self.on_auth_changed()
                
            messagebox.showinfo("Success", "Login successful!")
            self.app_controller.show_frame("profile")
            return True
        else:
            messagebox.showerror("Login Error", message)
            return False
    
    def handle_logout(self):
        """Handle user logout."""
        self.auth_manager.logout()
        self.app_controller.show_frame("welcome")
        return True
    
    def is_authenticated(self):
        """Check if user is authenticated."""
        return self.auth_manager.is_logged_in()
    
    def get_current_user(self):
        """Get the current logged in user."""
        return self.auth_manager.get_current_user()