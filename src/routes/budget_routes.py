from flask import Blueprint, render_template

budget_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budget_bp.route('/')
def budgets():
    return render_template('budget.html')