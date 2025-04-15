import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import os

# Set up path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Add src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ui.app_window import AppWindow 
from src.ui.login_frame import LoginFrame
from src.ui.register_frame import RegisterFrame
from src.ui.budget_frame import BudgetFrame 
from src.ui.report_frame import ReportFrame 
from src.ui.transaction_frame import TransactionFrame 

class BudgetFlowApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.title("BudgetFlow")
        self.geometry("800x600")
        self.minsize(800, 600)

        # Create a container for all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store frames
        self.frames = {}

        # Initialize the frames
        self.setup_frames()

        # Show the Welcome frame
        self.show_frame("welcome")

    def setup_frames(self):
        """Initialize all frames and add them to the frames dictionary"""
        # Welcome Frame
        app_window = AppWindow(self.container, self)
        self.frames["welcome"] = app_window
        app_window.grid(row=0, column=0, sticky="nsew")
        
        # Login Frame
        login_frame = LoginFrame(self.container, self)
        self.frames["login"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")
        
        # Register Frame
        register_frame = RegisterFrame(self.container, self)
        self.frames["register"] = register_frame
        register_frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """Show the frame with the given name"""
        frame = self.frames[frame_name]
        frame.tkraise()  # Bring the frame to the top

if __name__ == "__main__":
    app = BudgetFlowApp()
    app.mainloop()