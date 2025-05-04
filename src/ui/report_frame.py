import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from src.models.transaction import load_all_transactions

class ReportFrame(tk.Frame):
    """
    A frame for displaying financial reports using a tabbed interface.
    
    This class creates a UI for visualizing financial data including savings goals,
    weekly spending, and monthly comparisons. It uses matplotlib to generate
    charts embedded in a tkinter interface.
    
    Attributes:
        controller: The main application controller
        canvas: Background canvas for the frame
        notebook: Tabbed interface for different report types
        savings_tab: Tab for displaying savings goals progress
        weekly_tab: Tab for displaying weekly spending
        monthly_tab: Tab for displaying monthly spending comparisons
    """
    def __init__(self, parent, controller):
        """
        Initialize the ReportFrame with parent widget and controller.
        
        Args:
            parent: The parent widget
            controller: The main application controller for navigation
        """
        super().__init__(parent)
        self.controller = controller
        
        # Background canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)
        
        # Title text
        self.title_text = self.canvas.create_text(
            400, 50,
            text="Financial Reports",
            font=("Comic Sans MS", 24, "bold"),
            fill="#333333"
        )
        
        # Create notebook (tabbed interface) for different reports
        self.notebook = ttk.Notebook(self)
        
        # Store the window ID for later reference
        self.notebook_window = self.canvas.create_window(
            self.winfo_width()//2,  # Center horizontally
            self.winfo_height()//2, # Center vertically
            window=self.notebook, 
            width=self.winfo_width() * 0.85, 
            height=self.winfo_height() * 0.7
        )
        
        # Create tabs for different types of reports
        self.savings_tab = tk.Frame(self.notebook, bg="#f1e7e7")
        self.weekly_tab = tk.Frame(self.notebook, bg="#f1e7e7")
        self.monthly_tab = tk.Frame(self.notebook, bg="#f1e7e7")
        
        # Add tabs to notebook
        self.notebook.add(self.savings_tab, text="Savings Goals")
        self.notebook.add(self.weekly_tab, text="Weekly Spending")
        self.notebook.add(self.monthly_tab, text="Monthly Comparison")
        
        # Set up the content for each tab
        self.setup_savings_tab()
        self.setup_weekly_tab()
        self.setup_monthly_tab()
        
        # Back button to return to profile
        self.back_button = tk.Button(
            self,
            text="Back to Profile",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("profile")
        )
        self.back_button.place(x=350, y=550)
        
        # Add a refresh button
        self.refresh_button = tk.Button(
            self,
            text="Refresh Data",
            font=("Comic Sans MS", 12),
            bg="#d4fcd4",
            command=self.refresh_data
        )
        self.refresh_button.place(x=550, y=550)
        
        # Handle resize events
        self.bind("<Configure>", self.on_resize)
        
        # Bind custom event for refreshing data when frame is shown
        self.bind("<<FrameShown>>", lambda e: self.refresh_data())
    
    def on_resize(self, event):
        """
        Handle window resize events to ensure responsive layout.
        
        Adjusts the position and size of UI elements based on the new window dimensions.
        
        Args:
            event: The resize event containing window information
        """
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:  # Ensure window has size
            # Update canvas size
            self.canvas.config(width=width, height=height)
            
            # Reposition title text
            self.canvas.coords(self.title_text, width//2, 50)
            
            # Reposition AND resize notebook
            notebook_width = int(width * 0.85)  
            notebook_height = int(height * 0.7)  
            
            # Update both position and size of the notebook window
            self.canvas.coords(self.notebook_window, width//2, height//2)
            self.canvas.itemconfig(self.notebook_window, width=notebook_width, height=notebook_height)
            
            # Update back button position
            self.back_button.place(x=(width//2) - 150, y=height - 70)
            
            # Update refresh button position
            self.refresh_button.place(x=(width//2) + 50, y=height - 70)
    
    def setup_savings_tab(self):
        """
        Configure the Savings Goals tab with a pie chart.
        
        Creates a pie chart showing the distribution of savings across different categories.
        Displays a message if no savings data is available.
        """
        # Title for the tab
        tk.Label(
            self.savings_tab,
            text="Your Savings Goals Progress",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get user_id from controller
        user_id = None
        if hasattr(self.controller, 'auth_controller') and self.controller.auth_controller.is_authenticated():
            user_id = self.controller.auth_controller.get_current_user().id
        
        # Get savings goals data
        transactions = load_all_transactions(user_id)
        saving_transactions = [tx for tx in transactions if tx['type'].lower() == 'saving']
        
        if not saving_transactions:
            tk.Label(
                self.savings_tab,
                text="No savings goals data available yet.\nAdd savings in the Savings Goals section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))

        # Group by category and description
        categories = {}
        for tx in saving_transactions:
            category = tx['category']
            description = tx.get('description', '')
            amount = tx['amount']
            
            # Create a combined key for category and description
            label = category
            if description:
                label = f"{category} - {description}"
            
            if label in categories:
                categories[label] += amount
            else:
                categories[label] = amount
        
        # Create pie chart
        labels = list(categories.keys())
        sizes = list(categories.values())
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title('Savings Distribution by Category')
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(self.savings_tab, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def setup_weekly_tab(self):
        """
        Configure the Weekly Spending tab with a bar chart.
        
        Creates a bar chart showing expenses by category for the week.
        Displays a message if no expense data is available.
        """
        # Title for the tab
        tk.Label(
            self.weekly_tab,
            text="Weekly Spending by Category",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get user_id from controller
        user_id = None
        if hasattr(self.controller, 'auth_controller') and self.controller.auth_controller.is_authenticated():
            user_id = self.controller.auth_controller.get_current_user().id
        
        # Get transaction data
        transactions = load_all_transactions(user_id)
        expense_transactions = [tx for tx in transactions if tx['type'].lower() == 'expense']
        
        if not expense_transactions:
            tk.Label(
                self.weekly_tab,
                text="No expense data available yet.\nAdd expenses in the Transactions section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Group by category
        categories = {}
        for tx in expense_transactions:
            category = tx['category']
            amount = tx['amount']
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount
        
        # Create bar chart
        categories_list = list(categories.keys())
        amounts = list(categories.values())
        colors = plt.cm.Pastel2(np.linspace(0, 1, len(categories_list)))
        
        bars = ax.bar(categories_list, amounts, color=colors)
        ax.set_title('Weekly Spending by Category')
        ax.set_ylabel('Amount ($)')
        ax.set_xlabel('Category')
        plt.xticks(rotation=45, ha='right')
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'${height:.2f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.tight_layout()
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(self.weekly_tab, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def setup_monthly_tab(self):
        """
        Configure the Monthly Comparison tab with a stacked bar chart.
        
        Creates a stacked bar chart showing monthly spending by category.
        For demonstration purposes, this uses simulated data.
        Displays a message if no expense data is available.
        """
        # Title for the tab
        tk.Label(
            self.monthly_tab,
            text="Monthly Spending Comparison",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get user_id from controller
        user_id = None
        if hasattr(self.controller, 'auth_controller') and self.controller.auth_controller.is_authenticated():
            user_id = self.controller.auth_controller.get_current_user().id
        
        # Get transaction data
        transactions = load_all_transactions(user_id)
        expense_transactions = [tx for tx in transactions if tx['type'].lower() == 'expense']
        
        if not expense_transactions:
            tk.Label(
                self.monthly_tab,
                text="No expense data available yet.\nAdd expenses in the Transactions section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the stacked bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # For demo purposes, simulate monthly data if transaction dates aren't available
        # In a real application, we would use actual transaction dates
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        categories = set(tx['category'] for tx in expense_transactions)
        
        # Generate random data for demonstration
        data = {}
        for category in categories:
            data[category] = np.random.rand(len(months)) * 100  # Random values for demo
        
        # Create a stacked bar chart
        bottom = np.zeros(len(months))
        
        for category, values in data.items():
            p = ax.bar(months, values, bottom=bottom, label=category)
            bottom += values
        
        ax.set_title('Monthly Spending by Category')
        ax.set_ylabel('Amount ($)')
        ax.set_xlabel('Month')
        ax.legend(title='Categories')
        
        plt.tight_layout()
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(self.monthly_tab, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def refresh_data(self):
        """
        Refresh all report data.
        
        Clears and reloads all tabs with fresh data from the database
        based on the current user's ID.
        """
        # Clear all tabs
        for widget in self.savings_tab.winfo_children():
            widget.destroy()
        for widget in self.weekly_tab.winfo_children():
            widget.destroy()
        for widget in self.monthly_tab.winfo_children():
            widget.destroy()
            
        # Reload all tabs
        self.setup_savings_tab()
        self.setup_weekly_tab()
        self.setup_monthly_tab()