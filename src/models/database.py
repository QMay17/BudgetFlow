import sqlite3
from pathlib import Path
import os

# Get the project root directory
current_file = Path(__file__)
project_root = current_file.parent.parent.parent
data_dir = project_root / "data"
data_dir.mkdir(exist_ok=True)

# Define paths for two separate databases
USERS_DB_PATH = data_dir / "users.db"
TRANSACTIONS_DB_PATH = data_dir / "transactions.db"

### ---------- Connection Functions ----------

def get_users_db_connection():
    conn = sqlite3.connect(USERS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_transactions_db_connection():
    conn = sqlite3.connect(TRANSACTIONS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

### ---------- Initialization Functions ----------

def init_users_db():
    conn = get_users_db_connection()
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

def init_transactions_db():
    conn = get_transactions_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS savings_goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        target_amount REAL NOT NULL,
        deadline TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

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

    # Insert default categories
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

### ---------- Init All ----------

def initialize_all_databases():
    init_users_db()
    init_transactions_db()
    print("✅ All databases initialized.")

# Run when file is loaded
initialize_all_databases()
