import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.models.transaction import load_all_transactions
from datetime import datetime

class SavingsFrame(tk.Frame):
    """
    A frame for tracking and visualizing savings goals.
    
    This class provides a user interface for setting savings goals and visualizing
    progress towards these goals using interactive charts. Users can set a target amount,
    deadline, and category for their savings goals, and view their progress using
    either pie charts or bar charts.
    
    Attributes:
        controller: The main application controller
        saved_amount: The current amount saved towards the goal
        chart_canvas: The matplotlib canvas for displaying charts
        text_label: Label for displaying summary information about the savings goal
        canvas: Background canvas for the frame
        form_frame: Frame containing the input form elements
        chart_frame: Frame containing the visualization charts
    """
    def __init__(self, parent, controller):
        """
        Initialize the SavingsFrame with parent widget and controller.
        
        Sets up the UI layout with a form for input and an area for chart display.
        
        Args:
            parent: The parent widget
            controller: The main application controller for navigation
        """
        super().__init__(parent)
        self.controller = controller
        self.saved_amount = 0
        self.chart_canvas = None
        self.text_label = None

        # Set up the background
        self.configure(bg="#f1e7e7")
        
        # Create and place background canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)
        
        # Title text
        self.title_text = self.canvas.create_text(
            400, 30, 
            text="Savings Goal Tracker", 
            font=("Comic Sans MS", 24, "bold"), 
            fill="#333333"
        )
        
        # Create a frame for the form (left side)
        self.form_frame = tk.Frame(self, bg="#ffdddd", padx=20, pady=20)
        self.form_window = self.canvas.create_window(
            250, 270, 
            window=self.form_frame,
            width=500, 
            height=400,
            anchor="center"
        )
        
        # Form title
        form_title = tk.Label(
            self.form_frame, 
            text="Set Your Savings Goal",
            font=("Comic Sans MS", 14, "bold"),
            bg="#ffdddd",
            fg="#333333"
        )
        form_title.pack(pady=(0, 15), anchor="w")
        
        # Category
        category_frame = tk.Frame(self.form_frame, bg="#ffdddd")
        category_frame.pack(fill="x", pady=5)
        
        tk.Label(
            category_frame, 
            text="Category:",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333",
            width=20,
            anchor="w"
        ).pack(side="left")
        
        # Custom style for combobox
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff")
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        
        self.goal_dropdown = ttk.Combobox(
            category_frame,
            font=("Comic Sans MS", 12),
            values=["Vacation", "Emergency", "Education", "Car", "House", "Shopping"],
            width=20
        )
        self.goal_dropdown.set("Vacation")
        self.goal_dropdown.pack(side="left", padx=5)
        
        # Target Amount
        amount_frame = tk.Frame(self.form_frame, bg="#ffdddd")
        amount_frame.pack(fill="x", pady=5)
        
        tk.Label(
            amount_frame,
            text="Target Amount ($):",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333",
            width=20,
            anchor="w"
        ).pack(side="left")
        
        self.goal_amount_entry = tk.Entry(
            amount_frame, 
            font=("Comic Sans MS", 12), 
            width=20,
            bg="#ffffff",
            fg="black"
        )
        self.goal_amount_entry.pack(side="left", padx=5)
        
        # Deadline
        deadline_frame = tk.Frame(self.form_frame, bg="#ffdddd")
        deadline_frame.pack(fill="x", pady=5)
        
        tk.Label(
            deadline_frame,
            text="By When (YYYY-MM-DD):",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333",
            width=20,
            anchor="w"
        ).pack(side="left")
        
        self.deadline_entry = tk.Entry(
            deadline_frame, 
            font=("Comic Sans MS", 12), 
            width=20,
            bg="#ffffff",
            fg="black"
        )
        self.deadline_entry.pack(side="left", padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.form_frame, bg="#ffdddd")
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame,
            text="Show Pie Chart",
            font=("Comic Sans MS", 11),
            bg="#ffffff",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=self.show_pie_chart,
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Show Bar Chart",
            font=("Comic Sans MS", 11),
            bg="#ffffff",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=self.show_bar_chart,
            width=12
        ).pack(side="left", padx=5)
        
        # Create a frame for the chart (right side)
        self.chart_frame = tk.Frame(self, bg="#f1e7e7", padx=20, pady=20, relief="ridge", bd=2)
        self.chart_window = self.canvas.create_window(
            550, 270,  
            window=self.chart_frame,
            width=500,  
            height=400,  
            anchor="center"
        )
        
        # Navigation buttons
        self.nav_button_frame = tk.Frame(self, bg="#f1e7e7")
        self.nav_button_window = self.canvas.create_window(
            400, 550, 
            window=self.nav_button_frame,
            width=200, 
            height=50
        )
        
        tk.Button(
            self.nav_button_frame,
            text="Back to Profile",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=lambda: controller.show_frame("profile")
        ).pack(pady=10)


        self.text_label = tk.Label(
            self.canvas,
            text="",
            font=("Comic Sans MS", 10),
            bg="#f1e7e7",
            fg="#333333",
            wraplength=700,
            justify="center"
        )
        self.suggestion_window = self.canvas.create_window(
            400, 520,
            window=self.text_label,
            anchor="center"
        )
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """
        Handle window resize events to ensure responsive layout.
        
        Adjusts the position and size of UI elements based on the new window dimensions.
        This method ensures the UI remains usable at different window sizes.
        
        Args:
            event: The resize event containing window information
        """
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:
            # Update canvas size
            self.canvas.config(width=width, height=height)
            
            # Reposition title text - higher position
            title_y = 70
            self.canvas.coords(self.title_text, width/2, title_y)

            # Calculate content start position - ensure minimum space below title
            content_start_y = title_y + 70  # Minimum space below title
            
            # Use a percentage of remaining space for vertical positioning
            usable_height = height - content_start_y - 70  # Reserve space for button
            center_y = content_start_y + (usable_height / 2)
            
            # Calculate new positions for frames
            center = width/2
            max_half_distance = min(350, width/4)  
            left_pos = center - max_half_distance
            right_pos = center + max_half_distance
            
            # Resize and reposition frames 
            form_width = min(500, width * 0.45)  
            form_height = min(400, height * 0.6)  
            chart_width = min(500, width * 0.45)  
            chart_height = min(400, height * 0.6)  
            
            # Update form frame
            self.canvas.coords(self.form_window, left_pos, center_y)
            self.canvas.itemconfig(self.form_window, width=form_width, height=form_height)
            
            # Update chart frame
            self.canvas.coords(self.chart_window, right_pos, center_y)
            self.canvas.itemconfig(self.chart_window, width=chart_width, height=chart_height)
            
            # Update navigation buttons
            self.canvas.coords(self.nav_button_window, width/2, center_y + form_height/2 + 50)
    
    def show_pie_chart(self):
        """
        Display a pie chart showing savings progress.
        
        Creates and displays a pie chart comparing saved amount to remaining
        amount for the selected savings goal category. The chart includes
        percentage labels and a text summary of the savings progress.
        
        Validates user input before creating the chart.
        """
        self.clear_chart()
        category = self.goal_dropdown.get()
        try:
            goal_amount = float(self.goal_amount_entry.get())
            if goal_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for the goal amount.")
            return

        # Get user_id from controller
        user_id = None
        if hasattr(self.controller, 'auth_controller') and self.controller.auth_controller.is_authenticated():
            user_id = self.controller.auth_controller.get_current_user().id

        # Load transactions and calculate saved amount
        transactions = load_all_transactions(user_id)
        saved_total = sum(tx["amount"] for tx in transactions 
                          if tx["type"].lower() == "saving" 
                          and tx["category"].lower() == category.lower())
        
        remaining = max(0, goal_amount - saved_total)

        # Create pie chart
        fig, ax = plt.subplots(figsize=(4, 3.5))
        if saved_total > 0 or remaining > 0:  # Only create chart if there's data
            ax.pie(
                [saved_total, remaining], 
                labels=["Saved", "Remaining"], 
                autopct='%1.1f%%', 
                colors=["#ffb3b3", "#f5efef"],
                explode=(0.1, 0)
            )
            ax.set_title(f"Savings Progress for {category}")
        else:
            ax.text(0.5, 0.5, "No data to display", 
                   horizontalalignment='center', verticalalignment='center')
            ax.axis('off')

        # Display chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add summary text
        summary_text = f"Goal: ${goal_amount:.2f}\nSaved: ${saved_total:.2f}\nRemaining: ${remaining:.2f}"
        self.text_label = tk.Label(
            self.chart_frame, 
            text=summary_text,
            font=("Comic Sans MS", 12),
            bg="#fff8e0",
            fg="#333333"
        )
        self.text_label.pack(pady=5)

    def show_bar_chart(self):
        """
        Display a bar chart comparing weekly savings target to actual savings.
        
        Creates and displays a bar chart that shows the weekly savings rate
        needed to reach the goal by the deadline, compared to the current
        weekly savings rate. Includes a suggestion for achieving the goal.
        
        Validates user input before creating the chart, including date format
        and ensuring the deadline is in the future.
        """
        self.clear_chart()
        category = self.goal_dropdown.get()

        # Validate inputs
        try:
            goal_amount = float(self.goal_amount_entry.get())
            if goal_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for the goal amount.")
            return

        deadline = self.deadline_entry.get()
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            today = datetime.today()
            if deadline_date <= today:
                messagebox.showerror("Invalid Date", "Deadline must be in the future.")
                return
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return

        # Calculate weeks remaining
        days_remaining = (deadline_date - today).days
        weeks_remaining = max(1, days_remaining // 7)

        # Get user_id from controller
        user_id = None
        if hasattr(self.controller, 'auth_controller') and self.controller.auth_controller.is_authenticated():
            user_id = self.controller.auth_controller.get_current_user().id

        # Get saved amount
        transactions = load_all_transactions(user_id)
        saved_total = sum(tx["amount"] for tx in transactions 
                        if tx["type"].lower() == "saving" 
                        and tx["category"].lower() == category.lower())

        # Calculate weekly targets
        weekly_target = goal_amount / weeks_remaining
        current_week = (today - today.replace(day=1)).days // 7 or 1
        weekly_actual = saved_total / current_week

        # Clear chart area
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Chart only in chart_frame
        self.chart_canvas = FigureCanvasTkAgg(plt.figure(figsize=(4, 3.5)), master=self.chart_frame)
        fig, ax = plt.subplots(figsize=(4, 3.5))
        bars = ax.bar(["Weekly Target", "Weekly Saved"],
                    [weekly_target, weekly_actual],
                    color=["#fdd365", "#b0c4de"])
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5, f'${height:.2f}',
                    ha='center', va='bottom')
        ax.set_title("Weekly Savings Target vs Actual")
        ax.set_ylabel("Amount ($)")
        plt.tight_layout()

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(pady=10)

        #  Suggestion goes below chart_frame, into self (parent frame)
        remaining = max(0, goal_amount - saved_total)
        try:
            weekly_needed = remaining / weeks_remaining
        except ZeroDivisionError:
            weekly_needed = 0.0

        suggestion = f"You need to save ~${weekly_needed:.2f} per week to meet your goal by {deadline_date.strftime('%Y-%m-%d')}."
       

        # Destroy previous if exists
        if self.text_label and self.text_label.winfo_exists():
            self.text_label.destroy()

        self.text_label = tk.Label(
            self.canvas,  # attach to canvas
            text=suggestion,
            font=("Comic Sans MS", 10),
            bg="#f1e7e7",
            fg="#333333",
            wraplength=700,
            justify="center"
        )

        self.canvas.create_window(
            400, 520,  
            window=self.text_label,
            anchor="center"
        )

    def clear_chart(self):
        """
        Clear the chart display area.
        
        Removes any existing chart and text labels from the chart frame.
        This is called before drawing a new chart to ensure a clean display.
        """
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None
        if self.text_label and self.text_label.winfo_exists():
            self.text_label.destroy()
        self.text_label = None

