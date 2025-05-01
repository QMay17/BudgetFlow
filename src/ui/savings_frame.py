import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.models.transaction import load_all_transactions
from datetime import datetime

class SavingsFrame(tk.Frame):
    def __init__(self, parent, controller):
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
            550, 270,  # Adjust y-coordinate to match form frame
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
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Handle window resize event"""
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
        self.clear_chart()
        category = self.goal_dropdown.get()
        try:
            goal_amount = float(self.goal_amount_entry.get())
            if goal_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for the goal amount.")
            return

        # Load transactions and calculate saved amount
        transactions = load_all_transactions()
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
        
        # Get saved amount
        transactions = load_all_transactions()
        saved_total = sum(tx["amount"] for tx in transactions 
                          if tx["type"].lower() == "saving" 
                          and tx["category"].lower() == category.lower())
        
        # Calculate weekly targets
        weekly_target = goal_amount / weeks_remaining
        weekly_actual = saved_total / max(1, (today - today.replace(day=1)).days // 7)  # Current weekly average
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(4, 3.5))
        bars = ax.bar(
            ["Weekly Target", "Weekly Saved"], 
            [weekly_target, weekly_actual], 
            color=["#fdd365", "#b0c4de"]
        )
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + 5,
                f'${height:.2f}',
                ha='center', 
                va='bottom', 
                rotation=0
            )
            
        ax.set_title("Weekly Savings Target vs Actual")
        ax.set_ylabel("Amount ($)")
        plt.tight_layout()

        # Display chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Show smart suggestion
        remaining = max(0, goal_amount - saved_total)
        
        suggestion = f"You need to save ~${weekly_target:.2f} per week to meet your goal by {deadline_date.strftime('%Y-%m-%d')}."
        
        self.text_label = tk.Label(
            self.chart_frame, 
            text=suggestion, 
            font=("Comic Sans MS", 10), 
            bg="#fff8e0", 
            fg="#333333",
            wraplength=300
        )
        self.text_label.pack(pady=5)

    def clear_chart(self):
        """Clear the chart display area"""
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None
        if self.text_label:
            self.text_label.destroy()
            self.text_label = None