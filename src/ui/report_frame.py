import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from src.models.transaction import load_all_transactions

class ReportFrame(tk.Frame):
    def __init__(self, parent, controller):
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
        self.canvas.create_window(400, 300, window=self.notebook, width=700, height=450)
        
        # Create tabs for different types of reports
        self.savings_tab = tk.Frame(self.notebook, bg="#f1e7e7")
        self.weekly_tab = tk.Frame(self.notebook, bg="#f1e7e7") 
        self.monthly_tab = tk.Frame(self.notebook, bg="#f1e7e7")
        
        # Create content frames inside each tab
        self.savings_content = self.create_content_frame(self.savings_tab)
        self.weekly_content = self.create_content_frame(self.weekly_tab)
        self.monthly_content = self.create_content_frame(self.monthly_tab)
    
        # Add tabs to notebook
        self.notebook.add(self.savings_tab, text="Savings Goals")
        self.notebook.add(self.weekly_tab, text="Weekly Spending")
        self.notebook.add(self.monthly_tab, text="Monthly Comparison")
        
        # Set up the content for each tab
        self.setup_savings_tab()
        self.setup_weekly_tab()
        self.setup_monthly_tab()
        
        # Back button to return to profile
        back_button = tk.Button(
            self,
            text="Back to Profile",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("profile")
        )
        back_button.place(x=350, y=550)
        
        # Handle resize events
        self.bind("<Configure>", self.on_resize)
    

    def on_resize(self, event):
        """Handle window resize event"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:
            # Update canvas size
            self.canvas.config(width=width, height=height)
            
            # Reposition title text
            self.canvas.coords(self.title_text, width/2, 50)
            
            # Resize notebook
            window_items = self.canvas.find_withtag("window")
            if window_items:  # Check if the list is not empty
                self.canvas.coords(window_items[0], width/2, height/2)

    def create_content_frame(self, parent):
        """Create a simple content frame inside the given parent"""
        content_frame = tk.Frame(parent, bg="#f1e7e7")
        content_frame.pack(fill="both", expand=True)
        return content_frame

    def setup_savings_tab(self):
        """Set up the Savings Goals tab"""
        content_frame = self.savings_content
        
        # Title for the tab
        tk.Label(
            content_frame,
            text="Your Savings Goals Progress",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get savings goals data
        transactions = load_all_transactions()
        saving_transactions = [tx for tx in transactions if tx['type'].lower() == 'saving']
        
        if not saving_transactions:
            tk.Label(
                content_frame,
                text="No savings goals data available yet.\nAdd savings in the Savings Goals section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Group by category and name
        categories = {}
        for tx in saving_transactions:
            category = tx['category']
            name = tx.get('name', 'Unnamed')  # Get name if available, default to 'Unnamed'
            label = f"{category} - {name}"
            amount = tx['amount']
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
        ax.set_title('Savings Distribution by Category and Name')
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(content_frame, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add a refresh button
        refresh_button = tk.Button(
            content_frame,
            text="Refresh Data",
            font=("Comic Sans MS", 10),
            bg="#fffece",
            command=self.refresh_savings_tab
        )
        refresh_button.pack(pady=10)
    
    def refresh_savings_tab(self):
        """Refresh the savings tab content"""
        content_frame = self.scrollable_savings
        
        # Clear existing content
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        # Re-setup the tab
        self.setup_savings_tab()
    
    def setup_weekly_tab(self):
        """Set up the Weekly Spending tab"""
        content_frame = self.scrollable_weekly
        
        # Title for the tab
        tk.Label(
            content_frame,
            text="Weekly Spending by Category",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get transaction data
        transactions = load_all_transactions()
        expense_transactions = [tx for tx in transactions if tx['type'].lower() == 'expense']
        
        if not expense_transactions:
            tk.Label(
                content_frame,
                text="No expense data available yet.\nAdd expenses in the Transactions section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Group by category and name
        categories = {}
        for tx in expense_transactions:
            category = tx['category']
            name = tx.get('name', '')  # Get name if available
            label = f"{category} - {name}" if name else category
            amount = tx['amount']
            if label in categories:
                categories[label] += amount
            else:
                categories[label] = amount
        
        # Create bar chart
        categories_list = list(categories.keys())
        amounts = list(categories.values())
        colors = plt.cm.Pastel2(np.linspace(0, 1, len(categories_list)))
        
        bars = ax.bar(categories_list, amounts, color=colors)
        ax.set_title('Weekly Spending by Category and Name')
        ax.set_ylabel('Amount ($)')
        ax.set_xlabel('Category - Name')
        plt.xticks(rotation=45, ha='right')
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'${height:.2f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.tight_layout()
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(content_frame, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add a refresh button
        refresh_button = tk.Button(
            content_frame,
            text="Refresh Data",
            font=("Comic Sans MS", 10),
            bg="#fffece",
            command=self.refresh_weekly_tab
        )
        refresh_button.pack(pady=10)
    
    def refresh_weekly_tab(self):
        """Refresh the weekly tab content"""
        content_frame = self.scrollable_weekly
        
        # Clear existing content
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        # Re-setup the tab
        self.setup_weekly_tab()
    
    def setup_monthly_tab(self):
        """Set up the Monthly Comparison tab"""
        content_frame = self.scrollable_monthly
        
        # Title for the tab
        tk.Label(
            content_frame,
            text="Monthly Spending Comparison",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get transaction data
        transactions = load_all_transactions()
        expense_transactions = [tx for tx in transactions if tx['type'].lower() == 'expense']
        
        if not expense_transactions:
            tk.Label(
                content_frame,
                text="No expense data available yet.\nAdd expenses in the Transactions section.",
                font=("Comic Sans MS", 12),
                bg="#f1e7e7"
            ).pack(pady=100)
            return
        
        # Create a figure for the stacked bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Group transactions by month and category
        monthly_data = {}
        for tx in expense_transactions:
            # Try to get the date from the transaction
            date_str = tx.get('date')
            if date_str:
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    month = date.strftime('%b')
                    category = tx['category']
                    amount = tx['amount']
                    
                    if month not in monthly_data:
                        monthly_data[month] = {}
                    
                    if category not in monthly_data[month]:
                        monthly_data[month][category] = 0
                    
                    monthly_data[month][category] += amount
                except:
                    pass
        
        # If no valid date data, use simulated data
        if not monthly_data:
            # For demo purposes, simulate monthly data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            categories = set(tx['category'] for tx in expense_transactions)
            
            # Generate random data for demonstration
            data = {}
            for category in categories:
                data[category] = np.random.rand(len(months)) * 100  # Random values
            
            # Create a stacked bar chart with simulated data
            bottom = np.zeros(len(months))
            
            for category, values in data.items():
                p = ax.bar(months, values, bottom=bottom, label=category)
                bottom += values
        else:
            # Use actual data
            months = sorted(monthly_data.keys())
            categories = set()
            for month_data in monthly_data.values():
                categories.update(month_data.keys())
            
            # Create stacked bar chart with actual data
            bottom = np.zeros(len(months))
            
            for category in categories:
                values = [monthly_data.get(month, {}).get(category, 0) for month in months]
                p = ax.bar(months, values, bottom=bottom, label=category)
                bottom += np.array(values)
        
        ax.set_title('Monthly Spending by Category')
        ax.set_ylabel('Amount ($)')
        ax.set_xlabel('Month')
        ax.legend(title='Categories')
        
        plt.tight_layout()
        
        # Embed the chart in the tab
        chart_frame = tk.Frame(content_frame, bg="#f1e7e7")
        chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add a refresh button
        refresh_button = tk.Button(
            content_frame,
            text="Refresh Data",
            font=("Comic Sans MS", 10),
            bg="#fffece",
            command=self.refresh_monthly_tab
        )
        refresh_button.pack(pady=10)
    
    def refresh_monthly_tab(self):
        """Refresh the monthly tab content"""
        content_frame = self.scrollable_monthly
        
        # Clear existing content
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        # Re-setup the tab
        self.setup_monthly_tab()