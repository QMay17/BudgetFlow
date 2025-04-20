import tkinter as tk
from tkinter import ttk, messagebox

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # TEMP placeholder to avoid crashes
        tk.Label(self, text="Profile Summary Page (Coming Soon)").pack(pady=20)