"""
Application initialization module.

This module sets up a Tkinter desktop application and initializes the database.
It creates a data directory if it doesn't exist and configures the application
for database operations.
"""

import os
import tkinter as tk
from tkinter import ttk
from models.database import init_db

def setup_application():
    """
    Initialize the application environment and database.
    
    Creates the data directory if it doesn't exist and sets up the database
    connection for the application.
    
    Returns:
        tk.Tk: The initialized Tkinter root window.
    """
    # Create data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at {data_dir}")

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Database Application")
    root.geometry("800x600")
    
    # Initialize the database
    init_db()  # Removed app parameter as Tkinter doesn't need it
    print("Database setup complete.")
    
    return root

if __name__ == "__main__":
    app = setup_application()
    app.mainloop()