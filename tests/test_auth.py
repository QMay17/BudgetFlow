import unittest
import sqlite3
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from src.models.user import User
from src.core.auth import AuthManager
from src.controllers.auth_controller import AuthController

class TestAuth(unittest.TestCase):
    """Test cases for authentication functionality"""
    
    def setUp(self):
        """Set up test database and environment before each test"""
        # Create a test database file
        self.test_db_path = Path("test_users.db")
        
        # Mock the database connection to use the test database
        self.db_patcher = patch('src.models.database.USERS_DB_PATH', self.test_db_path)
        self.db_patcher.start()
        
        # Initialize the test database
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            phone_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()
        
        # Create auth manager for testing
        self.auth_manager = AuthManager()
        
        # Create a mock app controller
        self.app_controller = MagicMock()
        self.auth_controller = AuthController(self.app_controller)
    
    def tearDown(self):
        """Clean up after each test"""
        self.db_patcher.stop()
        if self.test_db_path.exists():
            os.remove(self.test_db_path)
    
    def test_user_creation_success(self):
        """Test successful user creation"""
        success, message = self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "Registration successful")
        self.assertIsNotNone(self.auth_manager.current_user)
        self.assertEqual(self.auth_manager.current_user.username, "testuser")
        self.assertEqual(self.auth_manager.current_user.email, "test@example.com")
        self.assertEqual(self.auth_manager.current_user.full_name, "Test User")
    
    def test_user_creation_duplicate_username(self):
        """Test user creation with duplicate username"""
        # Create the first user
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Try to create a user with the same username
        success, message = self.auth_manager.register_user(
            "testuser", "another@example.com", "Another User", "password123", "password123"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "username_exists")
    
    def test_user_creation_duplicate_email(self):
        """Test user creation with duplicate email"""
        # Create the first user
        self.auth_manager.register_user(
            "testuser1", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Try to create a user with the same email
        success, message = self.auth_manager.register_user(
            "testuser2", "test@example.com", "Another User", "password123", "password123"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "email_exists")
    
    def test_user_creation_password_mismatch(self):
        """Test user creation with mismatched passwords"""
        success, message = self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password456"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Passwords do not match")
    
    def test_user_creation_short_password(self):
        """Test user creation with a password that's too short"""
        success, message = self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "pass", "pass"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Password must be at least 6 characters long")
    
    def test_user_creation_missing_fields(self):
        """Test user creation with missing fields"""
        success, message = self.auth_manager.register_user(
            "", "test@example.com", "Test User", "password123", "password123"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "All fields are required")
    
    def test_login_success(self):
        """Test successful login"""
        # Create a test user first
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset current user
        self.auth_manager.current_user = None
        
        # Test login
        success, message = self.auth_manager.login("testuser", "password123")
        
        self.assertTrue(success)
        self.assertEqual(message, "Login successful")
        self.assertIsNotNone(self.auth_manager.current_user)
        self.assertEqual(self.auth_manager.current_user.username, "testuser")
    
    def test_login_invalid_username(self):
        """Test login with invalid username"""
        success, message = self.auth_manager.login("nonexistent", "password123")
        
        self.assertFalse(success)
        self.assertEqual(message, "Invalid username or password")
        self.assertIsNone(self.auth_manager.current_user)
    
    def test_login_invalid_password(self):
        """Test login with invalid password"""
        # Create a test user first
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset current user
        self.auth_manager.current_user = None
        
        # Test login with wrong password
        success, message = self.auth_manager.login("testuser", "wrongpassword")
        
        self.assertFalse(success)
        self.assertEqual(message, "Invalid username or password")
        self.assertIsNone(self.auth_manager.current_user)
    
    def test_logout(self):
        """Test user logout"""
        # Create and login a user
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Verify logged in
        self.assertTrue(self.auth_manager.is_logged_in())
        
        # Test logout
        self.assertTrue(self.auth_manager.logout())
        self.assertFalse(self.auth_manager.is_logged_in())
        self.assertIsNone(self.auth_manager.current_user)
    
    def test_is_logged_in(self):
        """Test is_logged_in method"""
        # Should be False initially
        self.assertFalse(self.auth_manager.is_logged_in())
        
        # Create a user and login
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Should be True after login
        self.assertTrue(self.auth_manager.is_logged_in())
        
        # Should be False after logout
        self.auth_manager.logout()
        self.assertFalse(self.auth_manager.is_logged_in())
    
    def test_get_current_user(self):
        """Test get_current_user method"""
        # Should be None initially
        self.assertIsNone(self.auth_manager.get_current_user())
        
        # Create a user and login
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Should return the user object after login
        current_user = self.auth_manager.get_current_user()
        self.assertIsNotNone(current_user)
        self.assertEqual(current_user.username, "testuser")
        
        # Should be None after logout
        self.auth_manager.logout()
        self.assertIsNone(self.auth_manager.get_current_user())
    
    # ---- Tests for the AuthController ----
    
    @patch('src.controllers.auth_controller.messagebox')
    def test_controller_registration_success(self, mock_messagebox):
        """Test successful registration through the controller"""
        result = self.auth_controller.handle_registration(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        self.assertTrue(result)
        mock_messagebox.showinfo.assert_called_once()
        self.app_controller.show_frame.assert_called_once_with("login")
    
    @patch('src.controllers.auth_controller.messagebox')
    def test_controller_registration_username_exists(self, mock_messagebox):
        """Test controller behavior when username already exists"""
        # Create a user first
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset mocks
        self.app_controller.reset_mock()
        
        # Configure mock to return 'yes' when askquestion is called
        mock_messagebox.askquestion.return_value = 'yes'
        
        # Try to register with the same username
        result = self.auth_controller.handle_registration(
            "testuser", "another@example.com", "Another User", "password123", "password123"
        )
        
        self.assertFalse(result)
        mock_messagebox.askquestion.assert_called_once()
        self.app_controller.show_frame.assert_called_once_with("login")
    
    @patch('src.controllers.auth_controller.messagebox')
    def test_controller_registration_email_exists(self, mock_messagebox):
        """Test controller behavior when email already exists"""
        # Create a user first
        self.auth_manager.register_user(
            "testuser1", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset mocks
        self.app_controller.reset_mock()
        
        # Configure mock to return 'yes' when askquestion is called
        mock_messagebox.askquestion.return_value = 'yes'
        
        # Try to register with the same email
        result = self.auth_controller.handle_registration(
            "testuser2", "test@example.com", "Another User", "password123", "password123"
        )
        
        self.assertFalse(result)
        mock_messagebox.askquestion.assert_called_once()
        self.app_controller.show_frame.assert_called_once_with("login")
    
    @patch('src.controllers.auth_controller.messagebox')
    def test_controller_login_success(self, mock_messagebox):
        """Test successful login through the controller"""
        # Create a test user first
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset current user and mocks
        self.auth_manager.logout()
        self.app_controller.reset_mock()
        
        # Test login through controller
        result = self.auth_controller.handle_login("testuser", "password123")
        
        self.assertTrue(result)
        mock_messagebox.showinfo.assert_called_once()
        self.app_controller.show_frame.assert_called_once_with("profile")
    
    @patch('src.controllers.auth_controller.messagebox')
    def test_controller_login_failure(self, mock_messagebox):
        """Test login failure through the controller"""
        result = self.auth_controller.handle_login("nonexistent", "password123")
        
        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_once()
        self.app_controller.show_frame.assert_not_called()
    
    def test_controller_logout(self):
        """Test logout through the controller"""
        # Create and login a user
        self.auth_manager.register_user(
            "testuser", "test@example.com", "Test User", "password123", "password123"
        )
        
        # Reset mocks
        self.app_controller.reset_mock()
        
        # Test logout through controller
        result = self.auth_controller.handle_logout()
        
        self.assertTrue(result)
        self.app_controller.show_frame.assert_called_once_with("welcome")
        self.assertFalse(self.auth_controller.is_authenticated())

if __name__ == '__main__':
    unittest.main()