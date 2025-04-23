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
from src.ui.profile_frame import ProfileFrame
from src.ui.report_frame import ReportFrame 
from src.ui.transaction_frame import TransactionFrame
from src.ui.savings_frame import SavingsFrame
from src.ui.savings_goal_frame import SavingsGoalFrame
from src.controllers.auth_controller import AuthController 

class BudgetFlowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController(self)
        
        # Configure the window
        self.title("BudgetFlow")
        self.geometry("800x600")
        self.minsize(800, 600) 
           
        # Create a container for all frames
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
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
        app_window.grid(row=3, column=3, sticky="nsew")
        
        # Login Frame
        login_frame = LoginFrame(self.container, self)
        self.frames["login"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")
        
        # Register Frame
        register_frame = RegisterFrame(self.container, self)
        self.frames["register"] = register_frame
        register_frame.grid(row=0, column=0, sticky="nsew")
        
        # Profile Frame
        profile_frame = ProfileFrame(self.container, self)
        self.frames["profile"] = profile_frame
        profile_frame.grid(row=0, column=0, sticky="nsew")
        
        # Transaction Frame
        transaction_frame = TransactionFrame(self.container, self)
        self.frames["transaction"] = transaction_frame
        transaction_frame.grid(row=0, column=0, sticky="nsew")
        
        # Savings Frame (just for transactions)
        savings_frame = SavingsFrame(self.container, self)
        self.frames["savings"] = savings_frame
        savings_frame.grid(row=0, column=0, sticky="nsew")

        # Savings Goal Frame 
        savings_goal_frame = SavingsGoalFrame(self.container, self)
        self.frames["savings_goal"] = savings_goal_frame
        savings_goal_frame.grid(row=0, column=0, sticky="nsew")
        
        # Report Frame (new)
        report_frame = ReportFrame(self.container, self)
        self.frames["report"] = report_frame
        report_frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """Show the frame with the given name"""
        frame = self.frames[frame_name]
        frame.tkraise()  # Bring the frame to the top

if __name__ == "__main__":
    app = BudgetFlowApp()

    def report_size():
        width = app.winfo_width()
        height = app.winfo_height()
        print(f"[DEBUG] App window size: {width} x {height}")
        app.after(2000, report_size)  # Repeats every 2 seconds

    app.after(500, report_size)  # Start measuring after window initializes
    app.mainloop()