import tkinter as tk 
import re
from tkinter import messagebox

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create and place background canvas
        self.canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        self.title_text = self.canvas.create_text(
            400, 100, 
            text="Register Page", 
            font=("Comic Sans MS", 24, "bold"), 
            fill="#333333"
        )

        # Create a frame for registration form (similar to login_frame)
        self.register_frame = tk.Frame(self, bg="#f1e7e7", bd=0, relief=tk.RAISED)
        
        # Position the registration frame
        self.register_frame.place(relx=0.5, rely=0.55, anchor="center", width=400, height=400)  
        
        # Dictionary to hold entry widgets
        self.entries = {}
        fields = ["Full Name", "Email", "Username", "Password", "Confirm Password"]

        # Create fields
        for i, field in enumerate(fields):
            tk.Label(
                self.register_frame, 
                text=f"{field}:", 
                font=("Comic Sans MS", 12),
                bg="#f1e7e7",
                fg="black"  # Explicit black color for text
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            show = "*" if "Password" in field else ""
            entry = tk.Entry(
                self.register_frame,
                font=("Comic Sans MS", 12),
                width=20,
                show=show,
                bg="#ffffff",  # White background for input boxes
                fg="black"     # Black text for input
            )
            
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            self.entries[field] = entry

        # Button frame for better layout (like in login_frame)
        button_frame = tk.Frame(self.register_frame, bg="#f1e7e7")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Register button (matching login button style)
        register_button = tk.Button(
            button_frame,
            text="Register",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=self.submit_registration,
            width=10
        )
        register_button.pack(pady=5)
        
        # Back button (matching login back button style)
        back_button = tk.Button(
            button_frame,
            text="Back",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("welcome"),
            width=10
        )
        back_button.pack(pady=5)
        
        # Position the registration frame
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
        
        # Bind resize event
        #self.bind("<Configure>", self.on_resize)
        
    

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_resize(self, event):
        """Handle window resize event"""
        if event:
            # Update canvas size
            self.canvas.config(width=event.width, height=event.height)
        
        # Get current window dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:  # Avoid division by zero or negative values
            # Reposition title text
            self.canvas.coords(self.title_text, width/2, height*0.12)  
            
            # Reposition registration frame
            self.register_frame.place_configure(relx=0.5, rely=0.55)  

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

        # Call AuthController to handle registration
        success = self.controller.auth_controller.handle_registration(
            user_data["Username"],
            user_data["Email"],
            user_data["Full Name"],
            user_data["Password"],
            user_data["Confirm Password"]
        )

        if success:
            print(" Registration successful !")
        else:
            print("Registration failed")
