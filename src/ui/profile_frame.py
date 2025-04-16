import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create and place background canvas
        self.canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        # Create elements on canvas - we'll use canvas.itemconfig to update positions later
        self.title_text = self.canvas.create_text(
            400, 100, 
            text="Profile Page", 
            font=("Comic Sans MS", 24, "bold"), 
            fill="#333333"
        )