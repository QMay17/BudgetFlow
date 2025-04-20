import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SavingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.saved_amount = 0
        self.savings_goal = 0  # User sets this

        # first this: Category selection
        tk.Label(self, text="Select Saving Category:").pack(pady=5)
        self.category_dropdown = ttk.Combobox(self, values=["Savings", "Vacation", "Emergency", "Education", "Other"])
        self.category_dropdown.set("Savings")
        self.category_dropdown.pack()

        # Set goal input
        tk.Label(self, text="Enter Savings Goal ($):").pack(pady=5)
        self.goal_entry = tk.Entry(self)
        self.goal_entry.pack()

        tk.Button(self, text="Set Goal", command=self.set_goal).pack(pady=5)

        
        # Amount saved input
        tk.Label(self, text="Amount Saved:").pack(pady=5)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        # Buttons
        tk.Button(self, text="Add Saving", command=self.add_saving).pack(pady=10)
        tk.Button(self, text="Show Pie Chart", command=self.show_pie_chart).pack(pady=5)
        tk.Button(self, text="Show Bar Chart", command=self.show_bar_chart).pack(pady=5)

        # Back to Profile button
        tk.Button(
            self,
            text="Back to Profile",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: self.controller.show_frame("profile")
        ).pack(pady=10)

    def set_goal(self):
        try:
            new_goal = float(self.goal_entry.get())
            if new_goal <= 0:
                raise ValueError
            self.savings_goal = new_goal
            messagebox.showinfo("Goal Set", f"Savings goal set to ${new_goal}")
            self.goal_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number for your savings goal.")

    def add_saving(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_dropdown.get()
            self.current_category = category 

            if categorize_input(category) == "saving":
                self.saved_amount += amount
                messagebox.showinfo("Success", f"Added ${amount} to savings.")
            else:
                messagebox.showwarning("Not a saving category", "This input is not categorized as saving.")

            self.amount_entry.delete(0, tk.END)
            self.category_dropdown.set("Savings")

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def show_pie_chart(self):
        if self.savings_goal <= 0:
            messagebox.showerror("No Goal Set", "Please set a savings goal first.")
            return

        saved = min(self.saved_amount, self.savings_goal)
        remaining = max(0, self.savings_goal - saved)

        category = getattr(self, "current_category", "your goal")  # fallback if nothing added yet

        fig, ax = plt.subplots()
        ax.pie([saved, remaining], labels=["Saved", "Remaining"], autopct='%1.1f%%')
        ax.set_title(f"Savings Progress for {category} (Goal: ${self.savings_goal:.2f})")
        self.display_chart(fig)

    def show_bar_chart(self):
        # Dummy weekly data for demo
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        goal = [100, 100, 100, 100]
        actual = [80, 60, 90, self.saved_amount]

        category = getattr(self, "current_category", "your goal")

        fig, ax = plt.subplots()
        ax.bar(weeks, goal, label="Goal", alpha=0.5)
        ax.bar(weeks, actual, label="Actual", alpha=0.7)
        ax.set_title("Weekly Savings Comparison for {category} ${self.savings_goal:.2f})")
        ax.legend()
        self.display_chart(fig)

    def display_chart(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

def categorize_input(category):
    savings_keywords = ["savings", "goal", "emergency", "vacation", "education"]
    return "saving" if category.lower() in savings_keywords else "expense"
