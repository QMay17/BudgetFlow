from .database import get_db_connection

def save_transaction(category, amount, trans_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (category, amount, type) VALUES (?, ?, ?)",
        (category, amount, trans_type)
    )

    conn.commit()
    conn.close()
