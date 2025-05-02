import os
import sqlite3
import unittest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.models import transaction

class TestTransactionFunctions(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("test_transactions.db")
        patcher = patch("src.models.database.TRANSACTIONS_DB_PATH", self.test_db_path)
        self.addCleanup(patcher.stop)
        patcher.start()

        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            created_at TEXT
        )""")
        conn.commit()
        conn.close()

    def tearDown(self):
        if self.test_db_path.exists():
            os.remove(self.test_db_path)

    def test_save_transaction_success(self):
        tx_id = transaction.save_transaction("Groceries", 25.0, "Expense", "Weekly shopping", user_id=1)
        self.assertIsInstance(tx_id, int)

    def test_save_transaction_negative_amount(self):
        tx_id = transaction.save_transaction("Food", -10.0, "Expense", "Invalid negative", user_id=1)
        self.assertIsNone(tx_id)

    def test_save_transaction_zero_amount(self):
        tx_id = transaction.save_transaction("Utilities", 0.0, "Expense", "Zero amount", user_id=1)
        self.assertIsNone(tx_id)

    def test_save_transaction_invalid_type(self):
        tx_id = transaction.save_transaction("Misc", 15.0, "Unknown", "Invalid type", user_id=1)
        self.assertIsNone(tx_id)

    def test_load_all_transactions(self):
        transaction.save_transaction("Groceries", 40.0, "Expense", user_id=1)
        transaction.save_transaction("Groceries", 10.0, "Saving", user_id=1)
        txs = transaction.load_all_transactions(user_id=1)
        self.assertEqual(len(txs), 2)

    def test_load_transactions_by_category(self):
        transaction.save_transaction("Rent", 1000.0, "Expense", user_id=1)
        txs = transaction.load_transactions_by_category("Rent", user_id=1)
        self.assertGreaterEqual(len(txs), 1)
        self.assertEqual(txs[0]["category"], "Rent")

    def test_load_transactions_by_type(self):
        transaction.save_transaction("Salary", 3000.0, "Income", user_id=1)
        txs = transaction.load_transactions_by_type("Income", user_id=1)
        self.assertTrue(any(tx["type"] == "Income" for tx in txs))

    def test_update_transaction(self):
        tx_id = transaction.save_transaction("Shopping", 75.0, "Expense", "Old shoes", user_id=1)
        success = transaction.update_transaction(tx_id, amount=90.0, description="New shoes")
        self.assertTrue(success)

    def test_delete_transaction(self):
        tx_id = transaction.save_transaction("DeleteTest", 5.0, "Expense", user_id=1)
        success = transaction.delete_transaction(tx_id)
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
