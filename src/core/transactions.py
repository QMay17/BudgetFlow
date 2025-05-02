from src.models import transaction


class TransactionManager:
    def __init__(self, user_id=1):
        self.user_id = user_id

    def add(self, category, amount, trans_type, description=None):
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if trans_type not in ["Saving", "Expense", "Income"]:
            return False, "Invalid transaction type"

        tx_id = transaction.save_transaction(category, amount, trans_type, description, self.user_id)
        if tx_id:
            return True, f"Transaction saved with ID {tx_id}"
        else:
            return False, "Failed to save transaction"

    def get_all(self):
        return transaction.load_all_transactions(user_id=self.user_id)

    def get_by_category(self, category):
        return transaction.load_transactions_by_category(category, user_id=self.user_id)

    def get_by_type(self, trans_type):
        return transaction.load_transactions_by_type(trans_type, user_id=self.user_id)

    def get_summary(self, summary_type="spending"):
        if summary_type == "spending":
            return transaction.get_spending_summary(user_id=self.user_id)
        elif summary_type == "saving":
            return transaction.get_savings_summary(user_id=self.user_id)
        else:
            return {}
