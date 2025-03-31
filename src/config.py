import os

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-budgetflow-app'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../data/budgetflow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configurations
    SESSION_COOKIE_SECURE = os.environ.get('ENVIRONMENT') == 'production'
    REMEMBER_COOKIE_SECURE = os.environ.get('ENVIRONMENT') == 'production'
    
    # Password hashing settings
    BCRYPT_LOG_ROUNDS = 12