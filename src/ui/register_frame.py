import tkinter as tk 
import re
from tkinter import messagebox

class RegisterFrame(tk.Frame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create and place background canvas
        self.canvas = tk.Canvas(self, width = 800, height = 600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill = "both", expand = True)

        self.canvas.create_text(
            400, 180, 
            text="Register Page", 
            font=("Comic Sans MS", 16), 
            fill="#333333"
        )


        # Dictionary to hold entry widgets
        self.entries = {}
        fields = ["Full Name", "Email", "Username", "Password", "Confirm Password"]

        y_pos = 220

        for field in fields:
            self.canvas.create_text(300, y_pos, text=field, anchor="w", font=("Arial", 10), fill="#000000")
            show = "*" if "Password" in field else ""
            entry = tk.Entry(self, show=show, width=30)
            entry_window = self.canvas.create_window(400, y_pos + 15, window=entry)
            self.entries[field] = entry
            y_pos += 50

        # Register button
        register_btn = tk.Button(self, text="Register", command=self.submit_registration)
        self.canvas.create_window(400, y_pos + 20, window=register_btn)

    def submit_registration(self):
        user_data = {k: v.get().strip() for k, v in self.entries.items()}

    # Check for empty fields
        for field, value in user_data.items():
            if value == "":
                messagebox.showerror("Missing Info", f"Please enter {field}.")
                return

    # Check if email is valid format
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, user_data["Email"]):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

    # Check that passwords match
        if user_data["Password"] != user_data["Confirm Password"]:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return

    # check for password length
        if len(user_data["Password"]) < 6:
            messagebox.showwarning("Weak Password", "Password should be at least 6 characters.")
            return

        print(" Registration Data Validated:", user_data)
        messagebox.showinfo("Success", "Registration validated!")