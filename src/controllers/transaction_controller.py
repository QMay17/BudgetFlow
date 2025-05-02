from src.models import transaction
from tkinter import messagebox

class TransactionController:
    def __init__(self, user_id=1):
        self.user_id = user_id

    def add_transaction(self, category, amount, trans_type, description=None):
        """Add a transaction and handle validation/results."""
        result = transaction.save_transaction(category, amount, trans_type, description, self.user_id)
        if result:
            return True, f"{trans_type} transaction saved."
        else:
            return False, "Failed to save transaction."

    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID."""
        success = transaction.delete_transaction(transaction_id)
        return success

    def update_transaction(self, transaction_id, **kwargs):
        """Update an existing transaction."""
        return transaction.update_transaction(transaction_id, **kwargs)

    def get_all_transactions(self):
        """Fetch all transactions for the user."""
        return transaction.load_all_transactions(self.user_id)

    def get_by_category(self, category):
        return transaction.load_transactions_by_category(category, self.user_id)

    def get_by_type(self, trans_type):
        return transaction.load_transactions_by_type(trans_type, self.user_id)

    def get_spending_summary(self):
        return transaction.get_spending_summary(self.user_id)

    def get_savings_summary(self):
        return transaction.get_savings_summary(self.user_id)

    def get_by_date_range(self, start_date, end_date):
        return transaction.load_transactions_by_date_range(start_date, end_date, self.user_id)
