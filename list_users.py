#!/usr/bin/env python3
"""
A simple script to list all users in the database.
Save this as list_users.py at the root of your project.
"""

import sqlite3
from pathlib import Path
import sys

def list_all_users():
    # Find the data directory (should be at project root)
    project_root = Path(__file__).parent
    db_path = project_root / "data" / "users.db"
    
    # Check if database exists
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("No users are registered yet.")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query all users
        cursor.execute("SELECT id, username, email, full_name, created_at FROM users")
        users = cursor.fetchall()
        
        # Print results
        if not users:
            print("No users found in the database.")
        else:
            print(f"Found {len(users)} user(s) in the database:")
            print("-" * 80)
            print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Full Name':<25} {'Created At'}")
            print("-" * 80)
            
            for user in users:
                print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {user['full_name']:<25} {user['created_at']}")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_all_users()