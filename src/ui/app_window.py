import tkinter as tk
from tkinter import ttk
from pathlib import Path

class AppWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set Background color
        self.configure(bg="#f1e7e7")    

        # Create and place background canvas
        self.canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        # Store canvas items as instance variables for easier access during resize
        self.subtitle_text = self.canvas.create_text(
            400, 180, 
            text="You are owning your own finance with", 
            font=("Comic Sans MS", 16), 
            fill="#333333"
        )
        
        self.title_text = self.canvas.create_text(
            400, 240, 
            text="BudgetFlow", 
            font=("Comic Sans MS", 36, "bold"), 
            fill="#333333"
        )

        # Tagline
        self.tagline_text = self.canvas.create_text(
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
            bg="#fffece"
        )
        self.login_button_window = self.canvas.create_window(400, 385, window=login_button)

        # Register button
        register_button = tk.Button(
            self,
            text="Register",
            font=("Comic Sans MS", 14),
            bd=0,
            command=lambda: controller.show_frame("register"),
            width=10,
            height=1,
            bg="#fffece"
        )
        self.register_button_window = self.canvas.create_window(400, 445, window=register_button)
        
        # Bind the resize event
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Handle window resize event"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Ensure the window has a valid size
        if width <= 1 or height <= 1:
            return
        
        # Update canvas size
        self.canvas.config(width=width, height=height)
        
        # Calculate new center positions
        center_x = width // 2
        center_y = height // 2
        
        # Reposition all elements based on the new center
        self.canvas.coords(self.subtitle_text, center_x, center_y - 120)
        self.canvas.coords(self.title_text, center_x, center_y - 60)
        self.canvas.coords(self.tagline_text, center_x, center_y - 5)
        
        # Reposition buttons
        self.canvas.coords(self.login_button_window, center_x, center_y + 80)
        self.canvas.coords(self.register_button_window, center_x, center_y + 145)