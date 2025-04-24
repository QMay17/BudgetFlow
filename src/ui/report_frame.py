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
        
        self.canvas.config(width=width, height=height)
        self.canvas.coords(self.title_text, width / 2, 50)

        # Fix: safely check before accessing index 0
        items = self.canvas.find_withtag("window")
        if items:
            self.canvas.coords(items[0], width / 2, height / 2)
    
    def setup_savings_tab(self):
        """Set up the Savings Goals tab"""
        # Title for the tab
        tk.Label(
            self.savings_tab,
            text="Your Savings Goals Progress",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get savings goals data
        transactions = load_all_transactions()
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
        
        # Group by category
        categories = {}
        for tx in saving_transactions:
            category = tx['category']
            amount = tx['amount']
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount
        
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
        """Set up the Weekly Spending tab"""
        # Title for the tab
        tk.Label(
            self.weekly_tab,
            text="Weekly Spending by Category",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get transaction data
        transactions = load_all_transactions()
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
        """Set up the Monthly Comparison tab"""
        # Title for the tab
        tk.Label(
            self.monthly_tab,
            text="Monthly Spending Comparison",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f1e7e7"
        ).pack(pady=10)
        
        # Get transaction data
        transactions = load_all_transactions()
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
        # In a real application, you would use actual transaction dates
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