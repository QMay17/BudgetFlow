
import tkinter as tk
from tkinter import ttk
from pathlib import Path

class AppWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set Background color
        self.configure(bg = "#f1e7e7")    

        # Create and place background canvas
        self.canvas = tk.Canvas(self, width = 800, height = 600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill = "both", expand = True)

        # Title and subtitle
        self.canvas.create_text(
            400, 180, 
            text="You are owning your own finance with", 
            font=("Comic Sans MS", 16), 
            fill="#333333"
        )
        
        self.canvas.create_text(
            400, 240, 
            text="BgetFlow", 
            font=("Comic Sans MS", 36, "bold"), 
            fill="#333333"
        )

        # Tagline
        self.canvas.create_text(
            400, 295, 
            text='"Your budget, your rules 🚀 Ready to take charge of your finances?"', 
            font=("Comic Sans MS", 12), 
            fill="#333333"
        )
        
        # Login button
        login_button = tk.Button(
            self,
            text="Login",
            font=("Comic Sans MS", 14),
            bd=0,
            command=lambda: controller.show_frame("login"),
            width=10,
            height=1,
            bg="#fffece"  # Updated color
        )
        login_button_window = self.canvas.create_window(400, 385, window=login_button)

        # Register button
        register_button = tk.Button(
            self,
            text="Register",
            font=("Comic Sans MS", 14),
            bd=0,
            command=lambda: controller.show_frame("register"),
            width=10,
            height=1,
            bg="#fffece"  # Updated color
        )
        register_button_window = self.canvas.create_window(400, 445, window=register_button)

    def on_resize(self, event):
        """Handle window resize event"""
        # Only resize if the window dimensions have actually changed
        if hasattr(self, 'width') and hasattr(self, 'height'):
            if self.width == event.width and self.height == event.height:
                return
        
        self.width, self.height = event.width, event.height
        
        # Resize the canvas to match frame size
        self.canvas.config(width=self.width, height=self.height)
        

        # Reposition the elements based on the new dimensions
        center_x, center_y = self.width // 2, self.height // 2
        
        # Reposition text
        self.canvas.coords(self.canvas.find_withtag("all")[1], center_x, center_y - 120)  # Title text
        self.canvas.coords(self.canvas.find_withtag("all")[2], center_x, center_y - 60)   # BudgetFlow text
        
        # Adjust the splash oval
        oval_coords = self.canvas.coords(self.canvas.find_withtag("all")[3])
        self.canvas.coords(
            self.canvas.find_withtag("all")[3], 
            center_x + 110, center_y - 75, 
            center_x + 135, center_y - 55
        )
        
        # Reposition tagline
        self.canvas.coords(self.canvas.find_withtag("all")[4], center_x, center_y - 5)
        
        # Reposition buttons
        self.canvas.coords(self.canvas.find_withtag("all")[5], center_x, center_y + 80)  # Login button
        self.canvas.coords(self.canvas.find_withtag("all")[6], center_x, center_y + 145)  # Register button
    
