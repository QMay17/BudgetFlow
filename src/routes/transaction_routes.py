from flask import Blueprint, render_template

transaction_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transaction_bp.route('/')
def transactions():
    return render_template('transaction.html')