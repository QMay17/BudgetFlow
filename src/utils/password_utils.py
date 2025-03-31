import random
import string

def generate_password(length=12):
    """Generate a random secure password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password