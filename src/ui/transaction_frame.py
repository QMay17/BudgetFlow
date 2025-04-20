import tkinter as tk
from tkinter import ttk, messagebox

class TransactionFrame(tk.Frame):
    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.transactions = []  # to store all transactions

        # Background canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        # Title text
        self.title_text = self.canvas.create_text(
            400, 70,
            text="Transaction Page",
            font=("Comic Sans MS", 24, "bold"),
            fill="#333333"
        )

        # --------- Input Form ---------
        self.form_frame = tk.Frame(self.canvas, bg="#f1e7e7")
        self.canvas.create_window(400, 150, window=self.form_frame, anchor="n")

        # Category
        tk.Label(self.form_frame, text="Category:", font=("Comic Sans MS", 12), bg="#f1e7e7").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.category_dropdown = ttk.Combobox(self.form_frame, font=("Comic Sans MS", 12),
                                              values=["Savings", "Vacation", "Emergency", "Education", "Food", "Rent", "Shopping"])
        self.category_dropdown.set("Savings")
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Amount
        tk.Label(self.form_frame, text="Amount ($):", font=("Comic Sans MS", 12), bg="#f1e7e7").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.amount_entry = tk.Entry(self.form_frame, font=("Comic Sans MS", 12), bg="#ffffff", fg="black")
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Type
        tk.Label(self.form_frame, text="Type:", font=("Comic Sans MS", 12), bg="#f1e7e7").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.type_dropdown = ttk.Combobox(self.form_frame, font=("Comic Sans MS", 12), values=["Saving", "Expense"])
        self.type_dropdown.set("Saving")
        self.type_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Add Button
        tk.Button(self.form_frame, text="Add Transaction", font=("Comic Sans MS", 12), bg="#fffece",
                  command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=15)

        # --------- Transaction Table ---------
        self.table_frame = tk.Frame(self.canvas, bg="#f1e7e7")
        self.canvas.create_window(400, 360, window=self.table_frame, anchor="n")

        # Treeview styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=25, font=("Comic Sans MS", 10))
        style.configure("Treeview.Heading", font=("Comic Sans MS", 11, "bold"))

        columns = ("Category", "Amount", "Type")
        self.transaction_table = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        for col in columns:
            self.transaction_table.heading(col, text=col)
            self.transaction_table.column(col, anchor="center", width=140)

        self.transaction_table.pack()

        # --------- Back Button ---------
        tk.Button(self.canvas, text="Back to Profile", font=("Comic Sans MS", 12), bg="#fffece",
                  command=lambda: controller.show_frame("profile")).place(x=320, y=580)

        # Resize handling
        self.bind("<Configure>", self.on_resize)
        self.update_idletasks()
        self.on_resize(None)

    def on_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        self.canvas.config(width=width, height=height)
        if width > 1 and height > 1:
            self.canvas.coords(self.title_text, width / 2, height * 0.08)

    def add_transaction(self):
        category = self.category_dropdown.get()
        amount_str = self.amount_entry.get()
        trans_type = self.type_dropdown.get()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        # Store in memory
        self.transactions.append({
            "category": category,
            "amount": amount,
            "type": trans_type
        })

        # Insert into table
        self.transaction_table.insert("", tk.END, values=(category, f"${amount:.2f}", trans_type))

        # Reset inputs
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.set("Savings")
        self.type_dropdown.set("Saving")
