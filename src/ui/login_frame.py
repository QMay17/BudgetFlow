import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class LoginFrame(tk.Frame):
    """
    Login screen for BudgetFlow application.
    
    This class creates the login interface with username and password fields,
    login and back buttons, and handles the authentication process.
    
    Attributes:
        controller: Reference to the main application controller
        canvas: Canvas widget for drawing text and containing the form
        login_frame: Frame containing the login form elements
        username_entry: Entry field for username input
        password_entry: Entry field for password input (masked with *)
    """
    def __init__(self, parent, controller):
        """
        Initialize the LoginFrame with all UI elements.
        
        Creates and positions the login form, title text, and navigation buttons.
        Sets up event binding for responsive layout.
        
        Args:
            parent: Parent widget that contains this frame
            controller: Application controller for navigation and authentication
        """
        super().__init__(parent)
        self.controller = controller
        
        # Create and place background canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)
        
        # Create elements on canvas 
        self.title_text = self.canvas.create_text(
            400, 100, 
            text="Login to BudgetFlow", 
            font=("Comic Sans MS", 24, "bold"), 
            fill="#333333"
        )
        
        # Create a frame for login form
        self.login_frame = tk.Frame(self, bg="#f1e7e7", bd=0, relief=tk.RAISED)
        
        # Username label and entry
        tk.Label(
            self.login_frame, 
            text="Username:", 
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"  # Added explicit black color for text
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.username_entry = tk.Entry(
            self.login_frame,
            font=("Comic Sans MS", 12),
            width=20,
            bg = "#ffffff",
            fg="black"
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Password label and entry
        tk.Label(
            self.login_frame, 
            text="Password:", 
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"  # Added explicit black color for text
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.password_entry = tk.Entry(
            self.login_frame,
            font=("Comic Sans MS", 12),
            width=20,
            show="*",
            bg = "#ffffff",
            fg="black"
        )
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Button frame for better layout
        button_frame = tk.Frame(self.login_frame, bg="#f1e7e7")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Login button
        login_button = tk.Button(
            button_frame,
            text="Login",
            font=("Comic Sans MS", 12),
            bg="#fffece",  # Updated color
            command=self.login,
            width=10
        )
        login_button.pack(pady=5)
        
        # Back button
        back_button = tk.Button(
            button_frame,
            text="Back",
            font=("Comic Sans MS", 12),
            bg="#fffece",  # Updated color
            command=lambda: controller.show_frame("welcome"),
            width=10
        )
        back_button.pack(pady=5)
        
        # Position the login frame
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=250)
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        
        # Initial resize to set positions
        self.update_idletasks()
        self.on_resize(None)
    
    def on_resize(self, event):
        """
        Handle window resize events to maintain responsive layout.
        
        Repositions the title and login form based on the new window dimensions,
        ensuring all elements remain properly centered and visible.
        
        Args:
            event: The Configure event containing new window dimensions.
                   Can be None during initial setup.
                   
        Returns:
            None: Early returns if window dimensions are invalid
        """
        if event:
            # Update canvas size
            self.canvas.config(width=event.width, height=event.height)
        
        # Get current window dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:  # Avoid division by zero or negative values
            # Reposition title text
            self.canvas.coords(self.title_text, width/2, height*0.25)
            
            # Reposition login frame
            self.login_frame.place_configure(relx=0.5, rely=0.5)
    
    def login(self):
        """
        Handle the login authentication process.
        
        Validates input fields, authenticates credentials through the auth controller,
        and navigates to the profile page on successful login. Shows an error message
        when validation fails.
        
        Returns:
            None: Early returns if validation fails
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return

        # Pass credentials to the auth controller
        success = self.controller.auth_controller.handle_login(username, password)

        if success:
            # Update profile information
            if "profile" in self.controller.frames:
                profile_frame = self.controller.frames["profile"]
                if hasattr(profile_frame, "update_profile_info"):
                    profile_frame.update_profile_info()
            
            # Navigate to profile page
            self.controller.show_frame("profile")
            
            # Clear entries for security
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)