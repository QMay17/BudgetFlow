from .database import get_savings_db_connection as get_db_connection
from datetime import datetime

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def save_saving(category, amount, description=None, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if user_id is None:
            user_id = 1  # Default fallback

        cursor.execute(
            "INSERT INTO transactions (user_id, category, amount, type, description, created_at) VALUES (?, ?, ?, 'Saving', ?, ?)",
            (user_id, category, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        print("Error saving saving:", e)
        conn.rollback()
        return None

    finally:
        conn.close()

def load_all_savings(user_id=None):
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    try:
        if user_id:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE type = 'Saving' AND user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ).fetchall()
        else:
            rows = cursor.execute(
                "SELECT * FROM transactions WHERE type = 'Saving' ORDER BY created_at DESC"
            ).fetchall()
        return rows

    except Exception as e:
        print("Error loading savings:", e)
        return []

    finally:
        conn.close()

def delete_saving(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print("Error deleting saving:", e)
        conn.rollback()
        return False

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
        print("Error getting savings summary:", e)
        return {}

    finally:
        conn.close()
