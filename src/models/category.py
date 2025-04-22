from .database import get_db_connection

def get_all_categories():
    """
    Get all budget categories from the database
    
    Returns:
        list: List of category dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        categories = cursor.execute(
            "SELECT id, name, type, description, color, icon FROM budget_categories ORDER BY name"
        ).fetchall()
        
        # Convert to list of dictionaries
        result = []
        for category in categories:
            result.append({
                'id': category['id'],
                'name': category['name'],
                'type': category['type'],
                'description': category['description'],
                'color': category['color'],
                'icon': category['icon']
            })
        
        return result
    
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []
    
    finally:
        conn.close()

def get_categories_by_type(category_type):
    """
    Get categories filtered by type (e.g., 'saving', 'expense')
    
    Args:
        category_type (str): Type to filter by
    
    Returns:
        list: List of category dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        categories = cursor.execute(
            "SELECT id, name, type, description, color, icon FROM budget_categories WHERE type = ? ORDER BY name",
            (category_type,)
        ).fetchall()
        
        # Convert to list of dictionaries
        result = []
        for category in categories:
            result.append({
                'id': category['id'],
                'name': category['name'],
                'type': category['type'],
                'description': category['description'],
                'color': category['color'],
                'icon': category['icon']
            })
        
        return result
    
    except Exception as e:
        print(f"Error getting categories by type: {e}")
        return []
    
    finally:
        conn.close()

def get_category_by_name(name):
    """
    Get a category by name
    
    Args:
        name (str): Category name
    
    Returns:
        dict: Category dictionary, or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        category = cursor.execute(
            "SELECT id, name, type, description, color, icon FROM budget_categories WHERE name = ?",
            (name,)
        ).fetchone()
        
        if category:
            return {
                'id': category['id'],
                'name': category['name'],
                'type': category['type'],
                'description': category['description'],
                'color': category['color'],
                'icon': category['icon']
            }
        else:
            return None
    
    except Exception as e:
        print(f"Error getting category by name: {e}")
        return None
    
    finally:
        conn.close()

def add_category(name, category_type, description=None, color=None, icon=None):
    """
    Add a new category to the database
    
    Args:
        name (str): Category name
        category_type (str): Category type (e.g., 'saving', 'expense')
        description (str, optional): Category description
        color (str, optional): Color hex code (e.g., '#76c7c0')
        icon (str, optional): Icon emoji or code
    
    Returns:
        int: ID of the inserted category, or None if failed
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO budget_categories (name, type, description, color, icon) VALUES (?, ?, ?, ?, ?)",
            (name, category_type, description, color, icon)
        )
        
        category_id = cursor.lastrowid
        conn.commit()
        return category_id
    
    except Exception as e:
        print(f"Error adding category: {e}")
        conn.rollback()
        return None
    
    finally:
        conn.close()

def update_category(category_id, name=None, category_type=None, description=None, color=None, icon=None):
    """
    Update a category in the database
    
    Args:
        category_id (int): ID of the category to update
        name (str, optional): New name
        category_type (str, optional): New type
        description (str, optional): New description
        color (str, optional): New color
        icon (str, optional): New icon
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the current category data
        current = cursor.execute(
            "SELECT * FROM budget_categories WHERE id = ?", 
            (category_id,)
        ).fetchone()
        
        if not current:
            return False
        
        # Update only the fields that were provided
        new_name = name if name is not None else current['name']
        new_type = category_type if category_type is not None else current['type']
        new_description = description if description is not None else current['description']
        new_color = color if color is not None else current['color']
        new_icon = icon if icon is not None else current['icon']
        
        cursor.execute(
            "UPDATE budget_categories SET name = ?, type = ?, description = ?, color = ?, icon = ? WHERE id = ?",
            (new_name, new_type, new_description, new_color, new_icon, category_id)
        )
        
        conn.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error updating category: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def delete_category(category_id):
    """
    Delete a category from the database
    
    Args:
        category_id (int): ID of the category to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if category is used in any transactions
        count = cursor.execute(
            "SELECT COUNT(*) FROM transactions WHERE category = (SELECT name FROM budget_categories WHERE id = ?)",
            (category_id,)
        ).fetchone()[0]
        
        if count > 0:
            # Don't delete categories that are in use
            return False
        
        cursor.execute("DELETE FROM budget_categories WHERE id = ?", (category_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    except Exception as e:
        print(f"Error deleting category: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def get_category_colors():
    """
    Get a mapping of category names to their colors
    
    Returns:
        dict: Dictionary with category name as key and color as value
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        categories = cursor.execute(
            "SELECT name, color FROM budget_categories"
        ).fetchall()
        
        return {category['name']: category['color'] for category in categories}
    
    except Exception as e:
        print(f"Error getting category colors: {e}")
        return {}
    
    finally:
        conn.close()