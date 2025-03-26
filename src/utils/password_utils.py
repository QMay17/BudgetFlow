import hashlib
import os

def hash_password(password):
    """
    Hash a password using SHA-256 and salt.
    
    Args:
        password (str): The plain text password to hash
    
    Returns:
        str: Hashed password with salt
    """
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the salt using SHA-256
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for hashing
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    
    # Combine salt and key
    storage = salt + key
    
    # Convert to hexadecimal representation
    return storage.hex()

def verify_password(stored_password, provided_password):
    """
    Verify a stored password against one provided by user
    
    Args:
        stored_password (str): The stored hashed password
        provided_password (str): The password provided by the user
    
    Returns:
        bool: True if password is correct, False otherwise
    """
    # Convert hex back to bytes
    storage = bytes.fromhex(stored_password)
    
    # Extract the salt (first 32 bytes)
    salt = storage[:32]
    
    # Hash the provided password with the extracted salt
    key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    
    # Combine salt and key
    new_storage = salt + key
    
    # Compare the newly created hash with the stored hash
    return new_storage.hex() == stored_password