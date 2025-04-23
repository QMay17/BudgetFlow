import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from src.models.transaction import load_all_transactions


class SavingsGoalFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f1e7e7")

        self.saved_amount = 0
        self.chart_canvas = None
        self.text_label = None

        # Title
        self.title_label = tk.Label(self, text="Savings Goal Tracker", font=("Comic Sans MS", 24, "bold"), bg="#f1e7e7", fg="#333333")
        self.title_label.pack(pady=20)

        # Main container
        main_frame = tk.Frame(self, bg="#f1e7e7")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Left: form
        self.form_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
        self.form_frame.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.9)

        # Goal inputs
        tk.Label(self.form_frame, text="What do you want to save for?", font=("Comic Sans MS", 12), bg="white").pack(pady=10)
        self.goal_dropdown = ttk.Combobox(self.form_frame, values=["Vacation", "Emergency", "Education", "Food", "Rent", "Shopping"])
        self.goal_dropdown.set("Vacation")
        self.goal_dropdown.pack()

        tk.Label(self.form_frame, text="How much do you want to save? ($)", font=("Comic Sans MS", 12), bg="white").pack(pady=10)
        self.goal_amount_entry = tk.Entry(self.form_frame)
        self.goal_amount_entry.pack()

        tk.Label(self.form_frame, text="By when? (YYYY-MM-DD)", font=("Comic Sans MS", 12), bg="white").pack(pady=10)
        self.deadline_entry = tk.Entry(self.form_frame)
        self.deadline_entry.pack()

        tk.Button(self.form_frame, text="Show Pie Chart", font=("Comic Sans MS", 10), bg="#d2f8d2", command=self.show_pie_chart).pack(pady=10)
        tk.Button(self.form_frame, text="Show Bar Chart", font=("Comic Sans MS", 10), bg="#cfe2ff", command=self.show_bar_chart).pack(pady=5)
        tk.Button(self.form_frame, text="Back to Profile", font=("Comic Sans MS", 10), bg="#fffece", command=lambda: self.controller.show_frame("profile")).pack(pady=20)

        # Right: Chart display
        self.chart_frame = tk.Frame(main_frame, bg="#f1e7e7")
        self.chart_frame.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.9)

    def show_pie_chart(self):
        self.clear_chart()
        category = self.goal_dropdown.get()
        try:
            goal_amount = float(self.goal_amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid goal amount.")
            return

        saved_total = sum(tx["amount"] for tx in load_all_transactions() if tx["type"].lower() == "saving" and tx["category"].lower() == category.lower())
        remaining = max(0, goal_amount - saved_total)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([saved_total, remaining], labels=["Saved", "Remaining"], autopct='%1.1f%%', colors=["#76c7c0", "#f7b7a3"])
        ax.set_title(f"Savings Progress for {category}")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack()

    def show_bar_chart(self):
        self.clear_chart()
        category = self.goal_dropdown.get()
        try:
            goal_amount = float(self.goal_amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid goal amount.")
            return

        deadline = self.deadline_entry.get()
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid date in YYYY-MM-DD format.")
            return

        today = datetime.today()
        weeks_remaining = max(1, (deadline_date - today).days // 7)
        saved_total = sum(tx["amount"] for tx in load_all_transactions() if tx["type"].lower() == "saving" and tx["category"].lower() == category.lower())

        weekly_target = goal_amount / weeks_remaining
        weekly_actual = saved_total / weeks_remaining

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(["Weekly Target", "Weekly Saved"], [weekly_target, weekly_actual], color=["#fdd365", "#b0c4de"])
        ax.set_title("Weekly Savings Target vs Actual")

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack()

        # Show smart suggestion
        remaining = max(0, goal_amount - saved_total)
        suggestion = f"You need to save ~${remaining/weeks_remaining:.2f} per week to meet your goal by {deadline}."
        self.text_label = tk.Label(self.chart_frame, text=suggestion, font=("Comic Sans MS", 10), bg="#f1e7e7", fg="#333")
        self.text_label.pack(pady=5)

    def clear_chart(self):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None
        if self.text_label:
            self.text_label.destroy()
            self.text_label = None