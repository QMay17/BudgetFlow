from .database import get_transactions_db_connection as get_db_connection
from datetime import datetime

def save_transaction(category, amount, trans_type, description=None, user_id=None):
    """
    Save a transaction to the database
    
    Args:
        category (str): Transaction category
        amount (float): Transaction amount
        trans_type (str): Transaction type (e.g., 'Saving', 'Expense')
        description (str, optional): Transaction description
        user_id (int): ID of the user making the transaction - REQUIRED
    
    Returns:
        int: ID of the inserted transaction, or None if failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Validate user_id is provided
        if user_id is None:
            print("[ERROR] user_id is required to save a transaction")
            return None
            
        # Validate amount is positive
        if amount <= 0:
            print("[ERROR] Amount must be greater than zero")
            return None
            
        cursor.execute(
            "INSERT INTO transactions (user_id, category, amount, type, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, category, amount, trans_type, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        
        transaction_id = cursor.lastrowid
        conn.commit()
        print(f"[DEBUG] ✅ Transaction saved → {trans_type} | {category} | ${amount:.2f} | user_id={user_id}")
        return transaction_id
    
    except Exception as e:
        print(f"Error saving transaction: {e}")
        conn.rollback()
        return None
    
    finally:
        conn.close()

def load_all_transactions(user_id=None):
    """
    Load all transactions from the database, optionally filtered by user_id
    
    Args:
        user_id (int, optional): ID of the user whose transactions to load
    
    Returns:
        list: List of transaction dictionaries
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory  # Convert rows to dictionaries
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ).fetchall()
            return rows
        else:
            # Return empty list when no user_id is provided
            return []
    
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []
    
    finally:
        conn.close()

def load_transactions_by_category(category, user_id=None):
    """
    Load transactions filtered by category
    
    Args:
        category (str): Category to filter by
        user_id (int, optional): ID of the user whose transactions to load
    
    Returns:
        list: List of transaction dictionaries
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions WHERE category = ? AND user_id = ? ORDER BY created_at DESC",
                (category, user_id)
            ).fetchall()
            return rows
        else:
            # Return empty list when no user_id is provided
            return []
    
    except Exception as e:
        print(f"Error loading transactions by category: {e}")
        return []
    
    finally:
        conn.close()

def load_transactions_by_type(trans_type, user_id=None):
    """
    Load transactions filtered by type (e.g., 'Saving', 'Expense')
    
    Args:
        trans_type (str): Type to filter by
        user_id (int, optional): ID of the user whose transactions to load
    
    Returns:
        list: List of transaction dictionaries
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions WHERE type = ? AND user_id = ? ORDER BY created_at DESC",
                (trans_type, user_id)
            ).fetchall()
            return rows
        else:
            # Return empty list when no user_id is provided
            return []
    
    except Exception as e:
        print(f"Error loading transactions by type: {e}")
        return []
    
    finally:
        conn.close()

def load_transactions_by_date_range(start_date, end_date, user_id=None):
    """
    Load transactions within a date range
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        user_id (int, optional): ID of the user whose transactions to load
    
    Returns:
        list: List of transaction dictionaries
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions WHERE date(created_at) BETWEEN date(?) AND date(?) AND user_id = ? ORDER BY created_at DESC",
                (start_date, end_date, user_id)
            ).fetchall()
            return rows
        else:
            # Return empty list when no user_id is provided
            return []
    
    except Exception as e:
        print(f"Error loading transactions by date range: {e}")
        return []
    
    finally:
        conn.close()

def delete_transaction(transaction_id):
    """
    Delete a transaction from the database
    
    Args:
        transaction_id (int): ID of the transaction to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def update_transaction(transaction_id, category=None, amount=None, trans_type=None, description=None):
    """
    Update a transaction in the database
    
    Args:
        transaction_id (int): ID of the transaction to update
        category (str, optional): New category
        amount (float, optional): New amount
        trans_type (str, optional): New type
        description (str, optional): New description
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the current transaction data
        current = cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,)).fetchone()
        
        if not current:
            return False
        
        # Update only the fields that were provided
        new_category = category if category is not None else current['category']
        new_amount = amount if amount is not None else current['amount']
        new_type = trans_type if trans_type is not None else current['type']
        new_description = description if description is not None else current['description']
        
        cursor.execute(
            "UPDATE transactions SET category = ?, amount = ?, type = ?, description = ? WHERE id = ?",
            (new_category, new_amount, new_type, new_description, transaction_id)
        )
        
        conn.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error updating transaction: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def get_spending_summary(user_id=None):
    """
    Get a summary of spending by category
    
    Args:
        user_id (int, optional): ID of the user whose transactions to summarize
    
    Returns:
        dict: Dictionary with category as key and total amount as value
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Expense' AND user_id = ? GROUP BY category",
                (user_id,)
            ).fetchall()
            return {row['category']: row['total'] for row in rows}
        else:
            # Return empty dict when no user_id is provided
            return {}
    
    except Exception as e:
        print(f"Error getting spending summary: {e}")
        return {}
    
    finally:
        conn.close()

def get_savings_summary(user_id=None):
    """
    Get a summary of savings by category
    
    Args:
        user_id (int, optional): ID of the user whose transactions to summarize
    
    Returns:
        dict: Dictionary with category as key and total amount as value
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if user_id is not None:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Saving' AND user_id = ? GROUP BY category",
                (user_id,)
            ).fetchall()
            return {row['category']: row['total'] for row in rows}
        else:
            # Return empty dict when no user_id is provided
            return {}
    
    except Exception as e:
        print(f"Error getting savings summary: {e}")
        return {}
    
    finally:
        conn.close()

def dict_factory(cursor, row):
    """
    Convert a row to a dictionary
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d