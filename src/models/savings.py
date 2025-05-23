from .database import get_transactions_db_connection as get_db_connection, dict_factory
from datetime import datetime
from src.models.transaction import *


def create_savings_goal(user_id, name, category, target_amount, deadline=None):
    """
    Create a new savings goal
    
    Args:
        user_id (int): ID of the user creating the goal
        name (str): Goal name
        category (str): Category for tracking associated transactions
        target_amount (float): Target amount to save
        deadline (str, optional): Deadline in YYYY-MM-DD format
        
    Returns:
        int: ID of the inserted goal, or None if failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO savings_goals (user_id, name, category, target_amount, deadline) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, category, target_amount, deadline)
        )
        
        goal_id = cursor.lastrowid
        conn.commit()
        return goal_id
    
    except Exception as e:
        print(f"Error creating savings goal: {e}")
        conn.rollback()
        return None
    
    finally:
        conn.close()

def get_all_savings_goals(user_id):
    """
    Get all savings goals for a user
    
    Args:
        user_id (int): User ID
        
    Returns:
        list: List of savings goal dictionaries
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        goals = cursor.execute(
            "SELECT * FROM savings_goals WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        
        return goals
    
    except Exception as e:
        print(f"Error getting savings goals: {e}")
        return []
    
    finally:
        conn.close()

def get_savings_goal(goal_id):
    """
    Get a savings goal by ID
    
    Args:
        goal_id (int): Goal ID
        
    Returns:
        dict: Savings goal dictionary, or None if not found
    """
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    try:
        goal = cursor.execute(
            "SELECT * FROM savings_goals WHERE id = ?",
            (goal_id,)
        ).fetchone()
        
        return goal
    
    except Exception as e:
        print(f"Error getting savings goal: {e}")
        return None
    
    finally:
        conn.close()

def update_savings_goal(goal_id, name=None, category=None, target_amount=None, deadline=None):
    """
    Update a savings goal
    
    Args:
        goal_id (int): Goal ID
        name (str, optional): New name
        category (str, optional): New category
        target_amount (float, optional): New target amount
        deadline (str, optional): New deadline in YYYY-MM-DD format
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the current goal data
        current = cursor.execute("SELECT * FROM savings_goals WHERE id = ?", (goal_id,)).fetchone()
        
        if not current:
            return False
        
        # Update only the fields that were provided
        new_name = name if name is not None else current['name']
        new_category = category if category is not None else current['category']
        new_target = target_amount if target_amount is not None else current['target_amount']
        new_deadline = deadline if deadline is not None else current['deadline']
        
        cursor.execute(
            "UPDATE savings_goals SET name = ?, category = ?, target_amount = ?, deadline = ? WHERE id = ?",
            (new_name, new_category, new_target, new_deadline, goal_id)
        )
        
        conn.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error updating savings goal: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()