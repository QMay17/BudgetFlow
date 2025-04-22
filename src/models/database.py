import sqlite3
from pathlib import Path 
import os 

# Get the project root directory
current_file = Path(__file__)
project_root = current_file.parent.parent.parent

# Create data directory at project root
data_dir = project_root / "data"
data_dir.mkdir(exist_ok=True)

# Database path
DB_Path = data_dir / "users.db"

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row  # to access column by name
    return conn

def init_db():
    """Initialize the database with necessary tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
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

    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create savings_goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS savings_goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        target_amount REAL NOT NULL,
        deadline TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create budget_categories table for predefined categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget_categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        color TEXT,
        icon TEXT
    )
    ''')
    
    # Insert default categories if none exist
    if cursor.execute("SELECT COUNT(*) FROM budget_categories").fetchone()[0] == 0:
        default_categories = [
            ("Savings", "saving", "General savings", "#76c7c0", "💰"),
            ("Vacation", "saving", "Vacation fund", "#fdd365", "🏖️"),
            ("Emergency", "saving", "Emergency fund", "#f7b7a3", "🚨"),
            ("Education", "saving", "Education fund", "#cfe2ff", "🎓"),
            ("Food", "expense", "Groceries and dining", "#ffcea9", "🍔"),
            ("Rent", "expense", "Housing costs", "#ffb1b1", "🏠"),
            ("Shopping", "expense", "Retail shopping", "#dcadff", "🛍️"),
            ("Transportation", "expense", "Public transit and gas", "#a9def9", "🚗"),
            ("Healthcare", "expense", "Medical expenses", "#d4f8d4", "🏥"),
            ("Personal", "expense", "Personal care", "#e7ceff", "💇"),
            ("Recreation", "expense", "Entertainment and hobbies", "#fcf7bb", "🎮")
        ]
        
        cursor.executemany(
            "INSERT INTO budget_categories (name, type, description, color, icon) VALUES (?, ?, ?, ?, ?)",
            default_categories
        )
    
    conn.commit()
    conn.close()

    print(f"Database initialized at {DB_Path}")

# Initialize the database when this module is imported
init_db()