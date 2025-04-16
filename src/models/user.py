import sqlite3
import hashlib
import os 
from pathlib import Path 
from datetime import datetime 
from .database import get_db_connection

class User:
    def __init__(self, username = None, email = None, full_name = None, password_hash = None, id = None, created_at = None):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password_hash = password_hash
        self_created_at = created_at or datetime.now()

    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256 with salt."""
        salt = os.urandom(32) # 32 bytes of random salt
        key = hashlib.pdkd2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000 # Number of iterations
        )
        # store salt and key together
        return salt.hex() + ':' + key.hex()
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a password against a stored hash"""
        # Split stored hash into salt and key
        salt_hex, key_hex = stored_password.split(':')
        salt = bytes.fromhex(salt_hex)

        # Hash the provided password with the same salt
        key = hashlib.pdkd2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )

        # Compared the computed key with the stored key
        return key.hex() == key_hex
    
    @classmethod
    def create(cls, username, email, full_name, password):
        """Create a new user in the database"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hash the password
        password_hash = cls.hash_password(password)

        try:
            cursor.execute(
                'INSERT INTO users(username, email, full_name, password_hash) VALUES(?, ?, ?, ?)'
                (username, email, full_name, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid

            # Fetch the created user
            user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id)).fetchone()
            return cls._row_to_user(user)
        except sqlite3.IntegrityError as e:
            # When username or email has already existed
            conn.rollback()
            if "UNIQUE constraint failed: users.username" in str(e):
                raise ValueError(f"Username '{username}' is already taken.")
            elif 'UNIQUE constraint failed: users.email' in str(e):
                raise ValueError(f"Email '{email}' is already in use. Would you like to login instead?")
            else:
                raise e
            
        finally:
            conn.close()

    @classmethod
    def find_by_usernmae(cls, username):
        """Find a user by username"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM username = ?', (username,)).fetchone()
        conn.close()
        return cls._row_to_user(user) if user else None
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email."""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return cls._row_to_user(user) if user else None
    
    @classmethod
    def _row_to_user(cls, row):
        """Convert a database row to a User object."""
        if not row:
            return None
        return cls(
            id = row['id'],
            username = row['username'],
            email = row['email'],
            full_name = row['full_name'],
            password_hash = row['password_hash'],
            created_at = row['created_at']
        )
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"