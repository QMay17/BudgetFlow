import datetime

def format_currency(amount, currency='$'):
    """Format a number as currency"""
    return f"{currency}{amount:,.2f}"

def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format a date object to string"""
    if isinstance(date_obj, datetime.datetime):
        return date_obj.strftime(format_str)
    return date_obj