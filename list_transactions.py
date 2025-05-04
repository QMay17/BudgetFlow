#!/usr/bin/env python3
"""
Script to diagnose database transaction user ID issues
"""

import sqlite3
from pathlib import Path

def get_db_connection():
    """Get a connection to the transactions database"""
    project_root = Path(__file__).parent
    db_path = project_root / "data" / "transactions.db"
    
    if not db_path.exists():
        print(f"Error: Database file not found at {db_path}")
        exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def diagnose_database():
    """Diagnose database structure and content"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("=== DATABASE DIAGNOSIS ===\n")
    
    # Check table structure
    print("TABLE STRUCTURE:")
    try:
        cursor.execute("PRAGMA table_info(transactions)")
        columns = cursor.fetchall()
        
        print("Transactions table columns:")
        for col in columns:
            print(f"  {col['name']} ({col['type']}) {'PRIMARY KEY' if col['pk'] else ''} {'NOT NULL' if col['notnull'] else ''}")
    except Exception as e:
        print(f"Error checking table structure: {e}")
    
    # Check if user_id column exists and is being used correctly
    print("\nUSER ID DISTRIBUTION:")
    try:
        cursor.execute("SELECT user_id, COUNT(*) as count FROM transactions GROUP BY user_id")
        user_counts = cursor.fetchall()
        
        if not user_counts:
            print("  No transactions found in the database.")
        else:
            for row in user_counts:
                print(f"  User ID {row['user_id']}: {row['count']} transactions")
    except Exception as e:
        print(f"Error checking user IDs: {e}")
    
    # Check if any NULL user_ids exist
    print("\nCHECKING FOR NULL USER IDS:")
    try:
        cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE user_id IS NULL")
        null_count = cursor.fetchone()['count']
        print(f"  Transactions with NULL user_id: {null_count}")
    except Exception as e:
        print(f"Error checking for NULL user IDs: {e}")
    
    # Sample some transactions to see what's happening
    print("\nSAMPLE TRANSACTIONS:")
    try:
        cursor.execute("SELECT id, user_id, category, amount, type, created_at FROM transactions LIMIT 5")
        samples = cursor.fetchall()
        
        if not samples:
            print("  No transactions found.")
        else:
            for tx in samples:
                print(f"  ID: {tx['id']}, User ID: {tx['user_id']}, Category: {tx['category']}, Amount: ${tx['amount']}, Type: {tx['type']}, Date: {tx['created_at']}")
    except Exception as e:
        print(f"Error fetching sample transactions: {e}")
        
    # Check users table (if it exists)
    print("\nUSERS TABLE CHECK:")
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        user_table_exists = cursor.fetchone() is not None
        
        if user_table_exists:
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            print(f"  Users table exists with {user_count} users")
            
            # List all users
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            print("\nREGISTERED USERS:")
            for user in users:
                print(f"  User ID: {user['id']}, Username: {user['username']}")
        else:
            print("  Users table does not exist in this database")
    except Exception as e:
        print(f"Error checking users table: {e}")
    
    conn.close()

if __name__ == "__main__":
    diagnose_database()