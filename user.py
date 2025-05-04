#!/usr/bin/env python3
"""
Script to delete specific users and their transactions from the database
"""

import sqlite3
import os
from pathlib import Path

def get_users_db_connection():
    """Get a connection to the users database"""
    project_root = Path(__file__).parent
    db_path = project_root / "data" / "users.db"
    
    if not db_path.exists():
        print(f"Error: Users database file not found at {db_path}")
        exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_transactions_db_connection():
    """Get a connection to the transactions database"""
    project_root = Path(__file__).parent
    db_path = project_root / "data" / "transactions.db"
    
    if not db_path.exists():
        print(f"Error: Transactions database file not found at {db_path}")
        exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def list_all_users():
    """List all users in the database"""
    conn = get_users_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, email FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if not users:
            print("No users found in the database.")
        else:
            print("\nExisting users:")
            for user in users:
                print(f"  ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")
    except Exception as e:
        print(f"Error listing users: {e}")
    finally:
        conn.close()

def delete_user(user_id):
    """Delete a user and their transactions"""
    # Delete from users database
    users_conn = get_users_db_connection()
    users_cursor = users_conn.cursor()
    
    # Delete from transactions database
    trans_conn = get_transactions_db_connection()
    trans_cursor = trans_conn.cursor()
    
    try:
        # First check if user exists
        users_cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = users_cursor.fetchone()
        
        if not user:
            print(f"User with ID {user_id} not found.")
            return False
        
        # Count associated transactions
        trans_cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE user_id = ?", (user_id,))
        tx_count = trans_cursor.fetchone()['count']
        
        # Delete transactions
        if tx_count > 0:
            trans_cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
            trans_conn.commit()
            print(f"Deleted {tx_count} transactions for user {user_id}.")
        else:
            print(f"No transactions found for user {user_id}.")
        
        # Delete user
        users_cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        users_conn.commit()
        
        print(f"Successfully deleted user {user_id} ({user['username']}).")
        return True
        
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        users_conn.rollback()
        trans_conn.rollback()
        return False
        
    finally:
        users_conn.close()
        trans_conn.close()

def reset_user_transactions(user_id):
    """Delete all transactions for a specific user without deleting the user"""
    conn = get_transactions_db_connection()
    cursor = conn.cursor()
    
    try:
        # Count transactions
        cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()['count']
        
        if count == 0:
            print(f"No transactions found for user {user_id}.")
            return True
            
        # Delete transactions
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        conn.commit()
        
        print(f"Successfully deleted {count} transactions for user {user_id}.")
        return True
        
    except Exception as e:
        print(f"Error resetting transactions for user {user_id}: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def main():
    print("==== USER AND TRANSACTION MANAGER ====\n")
    
    list_all_users()
    
    print("\nOptions:")
    print("  1. Delete user and their transactions")
    print("  2. Reset transactions for a user")
    print("  3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        user_id = input("Enter User ID to delete: ")
        try:
            user_id = int(user_id)
            confirm = input(f"Are you sure you want to delete user {user_id} and all their transactions? (y/n): ")
            if confirm.lower() == 'y':
                delete_user(user_id)
        except ValueError:
            print("Invalid input. Please enter a numeric User ID.")
    
    elif choice == '2':
        user_id = input("Enter User ID to reset transactions: ")
        try:
            user_id = int(user_id)
            confirm = input(f"Are you sure you want to delete all transactions for user {user_id}? (y/n): ")
            if confirm.lower() == 'y':
                reset_user_transactions(user_id)
        except ValueError:
            print("Invalid input. Please enter a numeric User ID.")
    
    elif choice == '3':
        print("Exiting...")
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()