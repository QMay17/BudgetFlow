import sqlite3
from pathlib import Path 
import os 

# Create data directory
data_dir = Path("data")
data_dir.mkdir(exist_ok = True)

# Database path
DB_Path = data_dir/"users.db"

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row # to access column by name
    return conn

def init_db():
    """Initialize the database with necessary tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMIARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        )
    ''')

    conn.commit()
    conn.close()

    print("Database initialized at {DB_PATH}")

# Initialize the database when this module is imported
init_db()
