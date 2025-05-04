import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import os

# Set up path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)  # Add src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ui.app_window import AppWindow
from src.ui.login_frame import LoginFrame
from src.ui.register_frame import RegisterFrame
from src.ui.profile_frame import ProfileFrame
from src.ui.report_frame import ReportFrame
from src.ui.transaction_frame import TransactionFrame
from src.ui.savings_frame import SavingsFrame
from src.controllers.auth_controller import AuthController
from src.controllers.transaction_controller import TransactionController


class BudgetFlowApp(tk.Tk):
    """
    Main application class for BudgetFlow.
    
    This class initializes the main application window and manages
    navigation between different frames. It serves as the container
    for all UI frames and handles the authentication controller.
    
    Attributes:
        auth_controller (AuthController): Controller handling user authentication
        container (tk.Frame): Main container for all frames
        frames (dict): Dictionary storing all UI frames
    """
    def __init__(self):
        """
        Initialize the BudgetFlow application.
        
        Sets up the main window configuration, creates the container frame,
        initializes all UI frames, and displays the welcome frame.
        """
        super().__init__()
        self.auth_controller = AuthController(self)
        self.transaction_controller = TransactionController(self.auth_controller.auth_manager)
        
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
        
        # Set up the window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_frames(self):
        """
        Initialize all frames and add them to the frames dictionary.
        
        Creates instances of all UI frames (welcome, login, register, profile,
        transaction, savings, report) and adds them to the frames dictionary
        for later access. Each frame is positioned in the same grid cell and
        will be raised to the top when needed.
        """
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
        
        # Profile Frame
        profile_frame = ProfileFrame(self.container, self)
        self.frames["profile"] = profile_frame
        profile_frame.grid(row=0, column=0, sticky="nsew")
        
        # Transaction Frame
        transaction_frame = TransactionFrame(self.container, self)
        self.frames["transaction"] = transaction_frame
        transaction_frame.grid(row=0, column=0, sticky="nsew")
        
        # Savings Frame 
        savings_frame = SavingsFrame(self.container, self)
        self.frames["savings"] = savings_frame
        savings_frame.grid(row=0, column=0, sticky="nsew")
        
        # Report Frame 
        report_frame = ReportFrame(self.container, self)
        self.frames["report"] = report_frame
        report_frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """
        Show the frame with the given name.
        
        Raises the specified frame to the top of the stacking order,
        making it visible to the user.
        
        Args:
            frame_name (str): The name of the frame to display
                             (e.g., "welcome", "login", "profile")
        """
        frame = self.frames[frame_name]
        frame.tkraise()
        
        # Trigger a custom event to notify the frame it's been shown
        # This allows frames to refresh their data when displayed
        frame.event_generate("<<FrameShown>>", when="tail")

    def on_close(self):
        """
        Handle window close event.
        
        Ensures proper cleanup before closing the application.
        """
        # Perform any cleanup needed before shutdown
        print("Application closing...")
        
        # Destroy the window and exit
        self.destroy()
        import sys
        sys.exit(0)


if __name__ == "__main__":
    app = BudgetFlowApp()
    app.mainloop()