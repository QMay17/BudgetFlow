from src.models import transaction
from tkinter import messagebox

class TransactionController:
    def __init__(self, auth_manager=None):
        """
        Initialize the transaction controller.
        
        Args:
            auth_manager: The authentication manager to get current user info
        """
        self.auth_manager = auth_manager
        self.user_id = None
        self.update_user_id()
    
    def update_user_id(self):
        """Update the controller with the current user's ID"""
        if self.auth_manager and self.auth_manager.current_user:
            self.user_id = self.auth_manager.current_user.id
            print(f"[DEBUG] TransactionController: Using user_id={self.user_id}")
        else:
            self.user_id = None
            print("[DEBUG] TransactionController: No user logged in")
    
    def add_transaction(self, category, amount, trans_type, description=None):
        """Add a transaction for the current user"""
        # Make sure we have a user ID
        if self.user_id is None:
            self.update_user_id()
            
        if self.user_id is None:
            return False, "No user is logged in. Please log in first."
            
        try:
            amount = float(amount)
        except ValueError:
            return False, "Invalid amount format."
            
        # Pass the current user's ID to the transaction model
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
        if not self.user_id:
            return []
        return transaction.load_all_transactions(self.user_id)

    def get_by_category(self, category):
        """Get transactions by category."""
        if not self.user_id:
            return []
        return transaction.load_transactions_by_category(category, self.user_id)

    def get_by_type(self, trans_type):
        """Get transactions by type."""
        if not self.user_id:
            return []
        return transaction.load_transactions_by_type(trans_type, self.user_id)

    def get_spending_summary(self):
        """Get summary of spending by category."""
        if not self.user_id:
            return {}
        return transaction.get_spending_summary(self.user_id)

    def get_savings_summary(self):
        """Get summary of savings by category."""
        if not self.user_id:
            return {}
        return transaction.get_savings_summary(self.user_id)

    def get_by_date_range(self, start_date, end_date):
        """Get transactions within a date range."""
        if not self.user_id:
            return []
        return transaction.load_transactions_by_date_range(start_date, end_date, self.user_id)