from datetime import datetime
from .database import get_transactions_db_connection as get_db_connection

# ---------- Utility ----------

def dict_factory(cursor, row):
    """
    Convert a row to a dictionary
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# ---------- Core Transaction Functions ----------

def save_transaction(category, amount, trans_type, description=None, user_id=None):
    """
    Save a transaction to the database
    """
    # Validate amount
    if not isinstance(amount, (int, float)) or amount <= 0:
        print(f"[ERROR]  Invalid amount: {amount}")
        return None

    # Validate transaction type
    valid_types = ["Saving", "Expense", "Income"]
    if trans_type not in valid_types:
        print(f"[ERROR]  Invalid transaction type: {trans_type}")
        return None

    if user_id is None:
        user_id = 1

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO transactions (user_id, category, amount, type, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, category, amount, trans_type, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        transaction_id = cursor.lastrowid
        conn.commit()
        print(f"[DEBUG] Transaction saved → {trans_type} | {category} | ${amount:.2f} | user_id={user_id}")
        return transaction_id
    except Exception as e:
        print(f"[ERROR] Failed to save transaction: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def load_all_transactions(user_id=None):
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT id, category, amount, type, description, created_at FROM transactions ORDER BY created_at DESC"
            ).fetchall()
        return rows
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []
    finally:
        conn.close()

def load_transactions_by_category(category, user_id=None):
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE category = ? AND user_id = ? ORDER BY created_at DESC",
                (category, user_id)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE category = ? ORDER BY created_at DESC",
                (category,)
            ).fetchall()
        return rows
    except Exception as e:
        print(f"Error loading transactions by category: {e}")
        return []
    finally:
        conn.close()

def load_transactions_by_type(trans_type, user_id=None):
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE type = ? AND user_id = ? ORDER BY created_at DESC",
                (trans_type, user_id)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE type = ? ORDER BY created_at DESC",
                (trans_type,)
            ).fetchall()
        return rows
    except Exception as e:
        print(f"Error loading transactions by type: {e}")
        return []
    finally:
        conn.close()

def load_transactions_by_date_range(start_date, end_date, user_id=None):
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE date(created_at) BETWEEN date(?) AND date(?) AND user_id = ? ORDER BY created_at DESC",
                (start_date, end_date, user_id)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE date(created_at) BETWEEN date(?) AND date(?) ORDER BY created_at DESC",
                (start_date, end_date)
            ).fetchall()
        return rows
    except Exception as e:
        print(f"Error loading transactions by date range: {e}")
        return []
    finally:
        conn.close()

def delete_transaction(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        print(f"[DEBUG]  Transaction deleted → id={transaction_id}")
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_transaction(transaction_id, category=None, amount=None, trans_type=None, description=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        current = cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,)).fetchone()
        if not current:
            return False
        new_category = category if category is not None else current['category']
        new_amount = amount if amount is not None else current['amount']
        new_type = trans_type if trans_type is not None else current['type']
        new_description = description if description is not None else current['description']

        cursor.execute(
            "UPDATE transactions SET category = ?, amount = ?, type = ?, description = ? WHERE id = ?",
            (new_category, new_amount, new_type, new_description, transaction_id)
        )
        conn.commit()
        print(f"[DEBUG]  Transaction updated → id={transaction_id}")
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating transaction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_spending_summary(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Expense' AND user_id = ? GROUP BY category",
                (user_id,)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Expense' GROUP BY category"
            ).fetchall()
        return {row['category']: row['total'] for row in rows}
    except Exception as e:
        print(f"Error getting spending summary: {e}")
        return {}
    finally:
        conn.close()

def get_savings_summary(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if user_id:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Saving' AND user_id = ? GROUP BY category",
                (user_id,)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT category, SUM(amount) as total FROM transactions WHERE type = 'Saving' GROUP BY category"
            ).fetchall()
        return {row['category']: row['total'] for row in rows}
    except Exception as e:
        print(f"Error getting savings summary: {e}")
        return {}
    finally:
        conn.close()