#!/usr/bin/env python3
"""
Script to display all transactions from the database
"""

import sqlite3
import os
from pathlib import Path

def get_db_connection():
    """Get a connection to the transactions database"""
    # Get the project root directory (assuming script is in project root)
    project_root = Path(__file__).parent
    db_path = project_root / "data" / "transactions.db"
    
    # Check if database exists
    if not db_path.exists():
        print(f"Error: Database file not found at {db_path}")
        exit(1)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def dict_factory(cursor, row):
    """Convert row to a dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def format_table(headers, data):
    """Format data as a table with columns of equal width"""
    # Calculate the width for each column based on the longest item
    col_widths = []
    for i in range(len(headers)):
        # Find the maximum width needed for this column
        header_width = len(str(headers[i]))
        max_data_width = max([len(str(row[i])) for row in data], default=0)
        col_widths.append(max(header_width, max_data_width) + 2)  # Add padding
    
    # Create the horizontal separator
    separator = "+"
    for width in col_widths:
        separator += "-" * width + "+"
    
    # Print the headers
    result = [separator]
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += str(header).center(col_widths[i]) + "|"
    result.append(header_row)
    result.append(separator)
    
    # Print the data
    for row in data:
        data_row = "|"
        for i, item in enumerate(row):
            data_row += str(item).center(col_widths[i]) + "|"
        result.append(data_row)
    
    result.append(separator)
    return "\n".join(result)

def view_all_transactions():
    """Display all transactions in the database"""
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        # Fetch all transactions ordered by most recent first
        transactions = cursor.execute(
            "SELECT id, user_id, category, amount, type, description, created_at FROM transactions ORDER BY created_at DESC"
        ).fetchall()
        
        if not transactions:
            print("No transactions found in the database.")
            return
        
        # Format the data for pretty printing
        table_data = []
        for tx in transactions:
            # Truncate description if it's too long
            description = tx['description'] or ""
            if description and len(description) > 20:
                description = description[:17] + "..."
                
            table_data.append([
                tx['id'],
                tx['category'],
                f"${tx['amount']:.2f}",
                tx['type'],
                description,
                tx['created_at'],
                tx['user_id']
            ])
        
        # Print using our custom table formatter
        headers = ["ID", "Category", "Amount", "Type", "Description", "Date", "User ID"]
        print(format_table(headers, table_data))
        print(f"\nTotal transactions: {len(transactions)}")
        
    except Exception as e:
        print(f"Error fetching transactions: {e}")
    
    finally:
        conn.close()

def get_transaction_summary():
    """Show summary of transactions by type and category"""
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        # Get total by type
        cursor.execute("SELECT type, SUM(amount) as total FROM transactions GROUP BY type")
        type_totals = cursor.fetchall()
        
        print("\n=== TRANSACTION SUMMARY ===")
        print("\nTotals by Type:")
        for row in type_totals:
            print(f"  {row['type']}: ${row['total']:.2f}")
        
        # Get total by category
        cursor.execute("SELECT category, type, SUM(amount) as total FROM transactions GROUP BY category, type")
        category_totals = cursor.fetchall()
        
        print("\nTotals by Category:")
        for row in category_totals:
            print(f"  {row['category']} ({row['type']}): ${row['total']:.2f}")
            
    except Exception as e:
        print(f"Error generating summary: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== TRANSACTION VIEWER ===")
    view_all_transactions()
    get_transaction_summary()