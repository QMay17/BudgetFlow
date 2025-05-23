import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class ProfileFrame(tk.Frame):
    """
    Profile page for the BudgetFlow application.
    
    This class creates and manages the user profile interface, displaying personal information
    and providing navigation to other sections of the application. It handles user profile data
    display and logout functionality.
    
    Attributes:
        controller: Reference to the main application controller
        canvas: Canvas widget for drawing text and containing the form
        profile_frame: Frame containing the profile information and navigation buttons
        welcome_label: Label displaying welcome message with user's name
        username_value: Label displaying the user's username
        full_name_value: Label displaying the user's full name
        email_value: Label displaying the user's email
    """
    def __init__(self, parent, controller):
        """
        Initialize the ProfileFrame with all UI elements.
        
        Creates and positions the profile information display, navigation buttons
        for different application sections, and sets up event binding for responsive layout.
        
        Args:
            parent: Parent widget that contains this frame
            controller: Application controller for navigation and authentication
        """
        super().__init__(parent)
        self.controller = controller
        
        # Create and place background canvas
        self.canvas = tk.Canvas(self, width=800, height=800, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)
        
        # Create elements on canvas
        self.title_text = self.canvas.create_text(
            400, 70, 
            text="My Profile", 
            font=("Comic Sans MS", 24, "bold"), 
            fill="#333333"
        )
        
        # Create a frame for profile information
        self.profile_frame = tk.Frame(self, bg="#f1e7e7", bd=0, relief=tk.RAISED)
        
        # User information labels
        self.welcome_label = tk.Label(
            self.profile_frame,
            text="Welcome!",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7",
            fg="black"
        )
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Username display
        tk.Label(
            self.profile_frame, 
            text="Username:", 
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.username_value = tk.Label(
            self.profile_frame,
            text="",  # Will be filled when user logs in
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        )
        self.username_value.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Full name display
        tk.Label(
            self.profile_frame, 
            text="Full Name:", 
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.full_name_value = tk.Label(
            self.profile_frame,
            text="",  # Will be filled when user logs in
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        )
        self.full_name_value.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Email display
        tk.Label(
            self.profile_frame, 
            text="Email:", 
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        ).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        self.email_value = tk.Label(
            self.profile_frame,
            text="",  # Will be filled when user logs in
            font=("Comic Sans MS", 12),
            bg="#f1e7e7",
            fg="black"
        )
        self.email_value.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Main button frame for navigation buttons
        main_button_frame = tk.Frame(self.profile_frame, bg="#f1e7e7")
        main_button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Report button
        report_button = tk.Button(
            main_button_frame,
            text="Go to Report",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("report"),
            width=15,
            relief=tk.RIDGE,
            bd=2
        )
        report_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Logout button
        logout_button = tk.Button(
            main_button_frame,
            text="Logout",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=self.logout,
            width=10,
            relief=tk.RIDGE,
            bd=2
        )
        logout_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Finance management buttons frame
        finance_button_frame = tk.Frame(self.profile_frame, bg="#f1e7e7")
        finance_button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Finance Buttons with consistent style and better spacing
        button_width = 15
        button_style = {"font": ("Comic Sans MS", 12), 
                        "bg": "#fffece", 
                        "relief": tk.RIDGE, 
                        "bd": 2,
                        "width": button_width}
        
        # Transaction Button (Report Finances)
        transaction_button = tk.Button(
            finance_button_frame,
            text="Report Finances",
            command=lambda: controller.show_frame("transaction"),
            **button_style
        )
        transaction_button.pack(pady=10)
        
        # Savings Goals Button
        savings_button = tk.Button(
            finance_button_frame,
            text="Saving Goals",
            command=lambda: controller.show_frame("savings"),
            **button_style
        )
        savings_button.pack(pady=10)
        
        # Finance Report Button
        report_details_button = tk.Button(
            finance_button_frame,
            text="Finance Report",
            command=lambda: controller.show_frame("report"),
            **button_style
        )
        report_details_button.pack(pady=10)
        
        # Position the profile frame with better placement
        self.profile_frame.place(relx=0.5, rely=0.48, anchor="center", width=400, height=480)
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        
        # Initial resize to set positions
        self.update_idletasks()
        self.on_resize(None)
    
    def on_resize(self, event):
        """
        Handle window resize events to maintain responsive layout.
        
        Repositions and resizes UI elements based on the new window dimensions,
        ensuring proper display across different screen sizes.
        
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
            self.canvas.coords(self.title_text, width/2, height * 0.1) 
            
            # Also adjust the profile frame for better proportions
            frame_width = min(400, width * 0.8)  # Responsive width
            frame_height = min(480, height * 0.7)  # Responsive height

            title_font_size = max(16, min(24, int(width / 30)))  # Between 16 and 24
            self.canvas.itemconfig(self.title_text, font=("Comic Sans MS", title_font_size, "bold"))
            
            # Reposition profile frame with better vertical alignment
            self.profile_frame.place_configure(
                relx=0.5, 
                rely=0.48,
                width=frame_width, 
                height=frame_height
            )
    
    def update_profile_info(self):
        """
        Update profile information display with current user data.
        
        Retrieves the current user from the authentication controller and updates
        the displayed information in the profile labels. Clears the display fields
        if no user is logged in.
        """
        # Get current user from auth controller
        current_user = self.controller.auth_controller.get_current_user()
        
        if current_user:
            # Update welcome message with user's name
            self.welcome_label.config(text=f"Welcome, {current_user.full_name}!")
            
            # Update user information
            self.username_value.config(text=current_user.username)
            self.full_name_value.config(text=current_user.full_name)
            self.email_value.config(text=current_user.email)
        else:
            # If no user is logged in, reset fields
            self.welcome_label.config(text="Welcome!")
            self.username_value.config(text="")
            self.full_name_value.config(text="")
            self.email_value.config(text="")
    
    def logout(self):
        """
        Handle the user logout process.
        
        Calls the authentication controller to log out the current user and
        resets all profile information fields to their default empty state.
        """
        # Call logout method from auth controller
        self.controller.auth_controller.handle_logout()
        
        # Reset profile information
        self.welcome_label.config(text="Welcome!")
        self.username_value.config(text="")
        self.full_name_value.config(text="")
        self.email_value.config(text="")