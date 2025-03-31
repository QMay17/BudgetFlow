from flask import Blueprint, render_template

report_bp = Blueprint('reports', __name__, url_prefix='/reports')

@report_bp.route('/')
def reports():
    return render_template('reports.html')