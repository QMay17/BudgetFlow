import tkinter as tk
from tkinter import ttk, messagebox
from src.models.transaction import (
    save_transaction, 
    load_all_transactions
)

class TransactionFrame(tk.Frame):
    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.transactions = []  # to store all transactions
        self.total_expenses = 0
        self.expense_categories = {
            "Living": 0,
            "Transportation": 0,
            "Healthcare": 0,
            "Groceries": 0,
            "Personal spending": 0,
            "Recreation": 0
        }
        self.savings = []  # to store all saving transactions
        self.total_savings = 0
        self.saving_categories = {
            "Vacation": 0,
            "Emergency": 0,
            "Education": 0,
            "Car": 0,
            "House": 0,
            "Shopping": 0
        }
        self.total_income = 0  
        self.income_types = ["Paycheck", "Investment", "Scholarships", "Bonuses", "Others"]
        self.saving_labels = {}  # Initialize the labels dictionary

        # Main background
        self.configure(bg="#f5efef")
        
        # Title text
        self.title_label = tk.Label(
            self,
            text="Budget Tracker",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f5efef",
            fg="#333333"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(15, 20), sticky="n")

        for i in range(6):  
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):  
            self.grid_columnconfigure(i, weight=1)

        # Create frames
        self.create_income_header()
        self.create_input_section()
        self.create_summary_section() #for expenses 
        self.create_savings_summary_section() #for savings 
        self.create_transaction_table()
        self.create_navigation_buttons()

        # Bind resize event
        self.bind("<Configure>", self.on_resize)

        # Initial resize call to set positions
        self.update_idletasks()
        self.on_resize(None)

        self.load_transaction_data()

    def load_transaction_data(self):
        """Load transaction data from the database and update the UI"""
        user_id = None
        if hasattr(self, 'user') and self.user:
            user_id = self.user.id
        
        # Clear existing transactions from the table
        for item in self.transaction_table.get_children():
            self.transaction_table.delete(item)
        
        # Reset summary values
        self.total_expenses = 0
        self.total_savings = 0
        for category in self.expense_categories:
            self.expense_categories[category].config(text="$0.00")
        for category in self.saving_labels:
            self.saving_labels[category].config(text="$0.00")
        
        # Load transactions from database
        transactions = load_all_transactions(user_id)
        if not transactions:
            return
        
        # Process each transaction
        for transaction in transactions:
            category = transaction['category']
            amount = transaction['amount']
            trans_type = transaction['type']
            
            # Add to table
            self.transaction_table.insert("", tk.END, values=(category, f"${amount:.2f}", trans_type))
            
            # Update the appropriate summary
            if trans_type == "Expense":
                if category in self.expense_categories:
                    current_text = self.expense_categories[category].cget("text")
                    current_amount = float(current_text.replace("$", "")) if current_text != "$0.00" else 0
                    new_amount = current_amount + amount
                    self.expense_categories[category].config(text=f"${new_amount:.2f}")
                    self.total_expenses += amount
            elif trans_type == "Saving":
                if category in self.saving_labels:
                    current_text = self.saving_labels[category].cget("text")
                    current_amount = float(current_text.replace("$", "")) if current_text != "$0.00" else 0
                    new_amount = current_amount + amount
                    self.saving_labels[category].config(text=f"${new_amount:.2f}")
                    self.total_savings += amount
            elif trans_type == "Income":
                self.total_income += amount
        
        # Update totals
        self.total_value.config(text=f"${self.total_expenses:.2f}")
        self.savings_total_value.config(text=f"${self.total_savings:.2f}")
        self.income_value.config(text=f"${self.total_income:.2f}")
        self.savings_income_value.config(text=f"${self.total_income:.2f}")

    def create_income_header(self):
        # Income header section
        self.income_frame = tk.Frame(self, bg="#f5efef")
        self.income_frame.grid(row=1, column=0, columnspan=4, pady=(0, 15), sticky="ew")
        
        self.budget_label = tk.Label(
            self.income_frame, 
            text="Budget",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f5efef",
            fg="#333333"
        )
        self.budget_label.grid(row=0, column=0, padx=(50, 20), sticky="w")
        
        # Replace paycheck button with dropdown
        self.income_type = tk.StringVar(value="Paycheck")
        self.income_dropdown = ttk.Combobox(
            self.income_frame,
            textvariable=self.income_type,
            values=self.income_types,
            font=("Comic Sans MS", 10),
            width=12,
            state="readonly"
        )
        self.income_dropdown.grid(row=0, column=1, padx=5)

        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        
        self.income_button = tk.Button(
            self.income_frame,
            text="Income",
            font=("Comic Sans MS", 10),
            bg="#ffffff",
            fg="#333333",
            relief="ridge",
            borderwidth=2
        )
        self.income_button.grid(row=0, column=2, padx=5)
        
        self.income_entry = tk.Entry(
            self.income_frame, 
            font=("Comic Sans MS", 10), 
            width=10,
            bg="#ffffff",
            fg="#000000"
        )
        self.income_entry.insert(0, str(self.total_income))
        self.income_entry.grid(row=0, column=3, padx=5)
        
        self.add_income_button = tk.Button(
            self.income_frame,
            text="Add",
            font=("Comic Sans MS", 10),
            bg="#ffffff",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=self.add_income
        )
        self.add_income_button.grid(row=0, column=4, padx=5)

    def create_input_section(self):
        # Left section - Expense input
        self.input_frame = tk.Frame(self, bg="#ffdddd", padx=20, pady=20, relief="flat")
        self.input_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        
        # Input section title
        input_title = tk.Label(
            self.input_frame, 
            text="Enter your transactions here...",
            font=("Comic Sans MS", 14),
            bg="#ffdddd",
            fg="#333333"
        )
        input_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # Name field
        tk.Label(
            self.input_frame, 
            text="Name:",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333"
        ).grid(row=1, column=0, pady=5, sticky="w")
        
        self.name_entry = tk.Entry(
            self.input_frame, 
            font=("Comic Sans MS", 12), 
            width=25,
            bg = "#ffffff",
            fg="black"
        )
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Category field
        tk.Label(
            self.input_frame,
            text="Categories:",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333"
        ).grid(row=2, column=0, pady=5, sticky="w")
        
        # Custom style for combobox
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff")
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        
        self.category_dropdown = ttk.Combobox(
            self.input_frame,
            font=("Comic Sans MS", 12),
            values=list(self.expense_categories.keys()),
            width=22
        )
        self.category_dropdown.set("Living")
        self.category_dropdown.grid(row=2, column=1, pady=5, padx=5)
        
        # Amount field
        tk.Label(
            self.input_frame,
            text="Amount:",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333"
        ).grid(row=3, column=0, pady=5, sticky="w")
        
        self.amount_entry = tk.Entry(
            self.input_frame, 
            font=("Comic Sans MS", 12), 
            width=25,
            bg = "#ffffff",
            fg="black"
        )
        self.amount_entry.grid(row=3, column=1, pady=5, padx=5)

        # Type dropdown (Expense or Saving)
        tk.Label(
            self.input_frame,
            text="Type:",
            font=("Comic Sans MS", 12),
            bg="#ffdddd",
            fg="#333333"
        ).grid(row=4, column=0, pady=5, sticky="w")

        self.type_var = tk.StringVar(value="Expense")  # default to Expense
        self.type_dropdown = ttk.Combobox(
            self.input_frame,
            textvariable=self.type_var,
            values=["Expense", "Saving"],
            font=("Comic Sans MS", 12),
            width=22,
            state="readonly"
        )

        self.type_dropdown.grid(row=4, column=1, pady=5, padx=5)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_category_dropdown)

        # Add button
        self.add_button = tk.Button(
            self.input_frame,
            text="Add",
            font=("Comic Sans MS", 11),
            bg="#ffffff",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=self.add_transaction,
            width=8
        )
        self.add_button.grid(row=5, column=1, pady=15, sticky="e")

    def update_category_dropdown(self, event=None):
        selected_type = self.type_var.get()
        if selected_type == "Expense":
            self.category_dropdown['values'] = list(self.expense_categories.keys())
            self.category_dropdown.set("Living")
        elif selected_type == "Saving":
            self.category_dropdown['values'] = list(self.saving_categories.keys())
            self.category_dropdown.set("Vacation")

    def create_summary_section(self):
        # Right section - Summary
        self.summary_frame = tk.Frame(
            self, 
            bg="#fff8e0", 
            padx=20, 
            pady=20, 
            relief="ridge", 
            bd=2
        )
        self.summary_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        
        # Total income
        self.income_container = tk.Frame(self.summary_frame, bg="#fff8e0")
        self.income_container.pack(fill="x", pady=2)
        
        tk.Label(
            self.income_container,
            text="⊙ Total income ...",
            font=("Comic Sans MS", 12),
            bg="#fff8e0",
            fg="#333333",
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.income_value = tk.Label(
            self.income_container,
            text=f"${self.total_income:.2f}",
            font=("Comic Sans MS", 12),
            bg="#fff8e0",
            fg="#333333",
            anchor="e"
        )
        self.income_value.pack(side="right", padx=5)
        
        # Create labels for each expense category
        for category in self.expense_categories:
            container = tk.Frame(self.summary_frame, bg="#fff8e0")
            container.pack(fill="x", pady=2)
            
            tk.Label(
                container,
                text=f"⊙ {category} ...",
                font=("Comic Sans MS", 12),
                bg="#fff8e0",
                fg="#333333",
                anchor="w"
            ).pack(side="left", padx=5)
            
            label = tk.Label(
                container,
                text="$0",
                font=("Comic Sans MS", 12),
                bg="#fff8e0",
                fg="#333333",
                anchor="e"
            )
            label.pack(side="right", padx=5)
            self.expense_categories[category] = label
        
        # Separator
        separator = tk.Frame(self.summary_frame, height=2, bg="#ffb3b3")  
        separator.pack(fill="x", pady=8)
        
        # Total expenses
        self.total_container = tk.Frame(self.summary_frame, bg="#ffb3b3")
        self.total_container.pack(fill="x", pady=2)
        
        tk.Label(
            self.total_container,
            text="Total expenses ...",
            font=("Comic Sans MS", 14),
            bg="#ffb3b3",
            fg="#ffffff",
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.total_value = tk.Label(
            self.total_container,
            text="$0",
            font=("Comic Sans MS", 14),
            bg="#ffb3b3",
            fg="#ffffff",
            anchor="e"
        )
        self.total_value.pack(side="right", padx=5)

    #for savings 
    def create_savings_summary_section(self):
        # Right section - Savings Summary
        self.savings_summary_frame = tk.Frame(
            self,
            bg="#fff8e0",
            padx=20,
            pady=20,
            relief="ridge",
            bd=2
        )
        self.savings_summary_frame.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")

        # Total income
        self.savings_income_container = tk.Frame(self.savings_summary_frame, bg="#fff8e0")
        self.savings_income_container.pack(fill="x", pady=2)

        tk.Label(
            self.savings_income_container,
            text="⊙ Total income ...",
            font=("Comic Sans MS", 12),
            bg="#fff8e0",
            fg="#333333",
            anchor="w"
        ).pack(side="left", padx=5)

        self.savings_income_value = tk.Label(
            self.savings_income_container,
            text=f"${self.total_income:.2f}",
            font=("Comic Sans MS", 12),
            bg="#fff8e0",
            fg="#333333",
            anchor="e"
        )
        self.savings_income_value.pack(side="right", padx=5)

        self.saving_labels = {} # To initialize the dictionary

        for category in self.saving_categories:
            container = tk.Frame(self.savings_summary_frame, bg="#fff8e0")
            container.pack(fill="x", pady=2)

            tk.Label(
                container,
                text=f"⊙ {category} ...",
                font=("Comic Sans MS", 12),
                bg="#fff8e0",
                fg="#333333",
                anchor="w"
            ).pack(side="left", padx=5)

            label = tk.Label(
                container,
                text="$0",
                font=("Comic Sans MS", 12),
                bg="#fff8e0",
                fg="#333333",
                anchor="e"
            )
            label.pack(side="right", padx=5)
            self.saving_labels[category] = label

        # Separator
        separator = tk.Frame(self.savings_summary_frame, height=2, bg="#ffb3b3")
        separator.pack(fill="x", pady=8)

        # Total Savings
        self.total_savings = 0
        self.savings_total_container = tk.Frame(self.savings_summary_frame, bg="#ffb3b3") 
        self.savings_total_container.pack(fill="x", pady=2)

        tk.Label(
            self.savings_total_container,
            text="Total savings ...",
            font=("Comic Sans MS", 14),
            bg="#ffb3b3",  
            fg="#ffffff",
            anchor="w"
        ).pack(side="left", padx=5)

        self.savings_total_value = tk.Label(
            self.savings_total_container,
            text="$0",
            font=("Comic Sans MS", 14),
            bg="#ffb3b3",  
            fg="#ffffff",
            anchor="e"
        )

        self.saving_labels[category] = label
        self.savings_total_value.pack(side="right", padx=5)

    def create_transaction_table(self):
        # Transaction table
        self.table_frame = tk.Frame(self, bg="#f5efef")
        self.table_frame.grid(row=3, column=0, columnspan=3, padx=30, pady=(30, 10), sticky="nsew")
 
        # Table with header style
        columns = ("Category", "Amount", "Type")
        
        # Create a style for the treeview headers - Changed to white with black text
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 11, "bold"), background="#ffffff", foreground="#000000")
        style.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25, background="#ffffff", fieldbackground="#ffffff", foreground="#000000")
        
        # Create a container for the table and scrollbar
        self.tree_container = tk.Frame(self.table_frame, bg="#ffffff")
        self.tree_container.pack(fill="both", expand=True)
        
        self.transaction_table = ttk.Treeview(
            self.tree_container,
            columns=columns,
            show="headings",
            height=6
        )
        
        scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.transaction_table.yview)
        self.transaction_table.configure(yscrollcommand=scrollbar.set)

        style = ttk.Style()
        style.configure("Vertical.TScrollbar", background="white", arrowcolor="black", 
                        troughcolor="white", bordercolor="white")
        scrollbar.configure(style="Vertical.TScrollbar")
        
        for col in columns:
            self.transaction_table.heading(col, text=col)
            self.transaction_table.column(col, anchor="center", width=140)
        
        self.transaction_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tip label for right-click
        tip_label = tk.Label(
            self,
            text="💡 Right-click a transaction row to edit or delete it.",
            font=("Comic Sans MS", 10),
            bg="#f5efef",
            fg="#333333"
        )
        tip_label.grid(row=4, column=0, columnspan=2, pady=3)
        
        # Right-click menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        
        # Bind right-click
        self.transaction_table.bind("<Button-3>", self.show_context_menu)

    def create_navigation_buttons(self):
        # Navigation buttons
        self.button_frame = tk.Frame(self, bg="#f5efef")
        self.button_frame.grid(row=5, column=0, columnspan=3, pady=20, sticky="n")
        
        tk.Button(
            self.button_frame,
            text="Back to Profile",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=lambda: self.controller.show_frame("profile")
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            self.button_frame,
            text="Save",
            font=("Comic Sans MS", 12),
            bg="#d4fcd4",
            fg="#333333",
            relief="ridge",
            borderwidth=2,
            command=self.finish_session
        ).grid(row=0, column=1, padx=10)


    def update_income(self):
        try:
            self.total_income = float(self.income_entry.get())
            self.income_value.config(text=f"${self.total_income:.2f}") #updates in expenses panel
            self.savings_income_value.config(text=f"${self.total_income:.2f}") # update sins savings panel
            
            messagebox.showinfo("Success", f"Income updated to ${self.total_income:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount for income.")

    # New method to add income from the dropdown
    def add_income(self):
        try:
            amount = float(self.income_entry.get())
            income_type = self.income_type.get()
            
            # Add to total income
            self.total_income += amount
            self.income_value.config(text=f"${self.total_income:.2f}")
            self.savings_income_value.config(text=f"${self.total_income:.2f}")#added
            
            # Add to transaction table
            self.transaction_table.insert("", tk.END, values=(income_type, f"${amount:.2f}", "Income"))
            
            # Save to database
            save_transaction(income_type, amount, "Income")
            
            # Clear income entry
            self.income_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", f"Added ${amount:.2f} from {income_type}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount for income.")

    def add_transaction(self):
        name = self.name_entry.get()
        category = self.category_dropdown.get()
        amount_str = self.amount_entry.get()

        if not name or not category or not amount_str:
            messagebox.showerror("Missing Information", "Please fill in all fields.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        trans_type = self.type_var.get()

        # Attempt to save to database
        transaction_id = save_transaction(category, amount, trans_type, description=name)
        if transaction_id is None:
            messagebox.showerror("Invalid Transaction", "Transaction was not saved. Please check your input.")
            return

        # Store in memory (only if saved)
        self.transactions.append({
            "name": name,
            "category": category,
            "amount": amount,
            "type": trans_type
        })

        # Insert into table
        self.transaction_table.insert("", tk.END, values=(category, f"${amount:.2f}", trans_type))

        # Update summary
        self.update_summary(category, amount, trans_type)

        # Reset inputs
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.update_category_dropdown()

        messagebox.showinfo("Success", f"Added ${amount:.2f} to {category}")

    def update_summary(self, category, amount, trans_type="Expense"):
        # Update category amount
        if trans_type == "Expense":
            if category in self.expense_categories:
                current_text = self.expense_categories[category].cget("text")
                current_amount = float(current_text.replace("$", ""))
                new_amount = current_amount + amount
                self.expense_categories[category].config(text=f"${new_amount:.2f}")
                # Update total
                self.total_expenses += amount
                self.total_value.config(text=f"${self.total_expenses:.2f}")
        elif trans_type == "Saving":
            if category in self.saving_labels:
                current_text = self.saving_labels[category].cget("text")
                current_amount = float(current_text.replace("$", ""))
                new_amount = current_amount + amount
                self.saving_labels[category].config(text=f"${new_amount:.2f}")
                #update total
                self.total_savings += amount
                self.savings_total_value.config(text=f"${self.total_savings:.2f}")
    
    def show_context_menu(self, event):
        # Select the row under mouse before showing menu
        item_id = self.transaction_table.identify_row(event.y)
        if item_id:
            self.transaction_table.selection_set(item_id)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected(self):
        selected = self.transaction_table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a transaction to delete.")
            return

        item = self.transaction_table.item(selected[0])
        values = item['values']
        category, amount_text, trans_type = values
        amount = float(amount_text.strip("$"))

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {trans_type.lower()} of ${amount:.2f} in '{category}'?")
        if not confirm:
            return

        # Delete from DB 
        from src.models.database import get_transactions_db_connection as get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM transactions 
        WHERE rowid = (
            SELECT rowid FROM transactions 
            WHERE category=? AND amount=? AND type=?
            LIMIT 1
        )
        """, (category, amount, trans_type))
        conn.commit()
        conn.close()

        # Update summary
        if trans_type == "Expense" and category in self.expense_categories:
            current_text = self.expense_categories[category].cget("text")
            current_amount = float(current_text.replace("$", ""))
            new_amount = current_amount - amount
            self.expense_categories[category].config(text=f"${new_amount:.2f}")
            
            # Update total
            self.total_expenses -= amount
            self.total_value.config(text=f"${self.total_expenses:.2f}")
        elif trans_type == "Income":
            # Update total income in BOTH panels
            self.total_income -= amount
            self.income_value.config(text=f"${self.total_income:.2f}")
            self.savings_income_value.config(text=f"${self.total_income:.2f}")

        elif trans_type == "Saving" and category in self.saving_labels:
            current_text = self.saving_labels[category].cget("text")
            current_amount = float(current_text.replace("$", ""))
            new_amount = current_amount - amount
            self.saving_labels[category].config(text=f"${new_amount:.2f}")
            self.total_savings -= amount
            self.savings_total_value.config(text=f"${self.total_savings:.2f}")

        # Delete from table
        self.transaction_table.delete(selected[0])
        messagebox.showinfo("Deleted", "Transaction deleted.")

    def edit_selected(self):
        selected = self.transaction_table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a transaction to edit.")
            return

        item = self.transaction_table.item(selected[0])
        values = item['values']
        category, amount_text, trans_type = values
        amount = float(amount_text.strip("$"))

        # Remove original entry from table 
        self.transaction_table.delete(selected[0])

        # Subtract from the appropriate summary
        if trans_type == "Expense":
            if category in self.expense_categories:
                current_text = self.expense_categories[category].cget("text")
                current_amount = float(current_text.replace("$", ""))
                new_amount = current_amount - amount
                self.expense_categories[category].config(text=f"${new_amount:.2f}")
                self.total_expenses -= amount
                self.total_value.config(text=f"${self.total_expenses:.2f}")

            self.type_var.set("Expense")  # Set dropdown
        elif trans_type == "Income":
            self.total_income -= amount
            self.income_value.config(text=f"${self.total_income:.2f}")
            if category in self.income_types:
                self.income_type.set(category)
            self.income_entry.delete(0, tk.END)
            self.income_entry.insert(0, amount_text.strip("$"))
            self.type_var.set("Income")
        elif trans_type == "Saving":
            if category in self.saving_labels:
                current_text = self.saving_labels[category].cget("text")
                current_amount = float(current_text.replace("$", ""))
                new_amount = current_amount - amount
                self.saving_labels[category].config(text=f"${new_amount:.2f}")
                
                self.total_savings -= amount
                self.savings_total_value.config(text=f"${self.total_savings:.2f}")
            self.type_var.set("Saving")

        # Pre-fill shared input fields
        self.category_dropdown.set(category)
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, amount_text.strip("$"))

        # Remove from database
        from src.models.database import get_transactions_db_connection as get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM transactions 
        WHERE rowid = (
            SELECT rowid FROM transactions 
            WHERE category=? AND amount=? AND type=?
            LIMIT 1
        )
        """, (category, amount, trans_type))
        conn.commit()
        conn.close()

        messagebox.showinfo("Edit Mode", f"Now modify the inputs and click 'Add' to re-save the {trans_type.lower()}.")

    def finish_session(self):
        messagebox.showinfo("Save", "All transactions saved!")
        self.controller.show_frame("profile")

    def on_resize(self, event):
        """Handle window resize events for the TransactionFrame"""
        # Get current window dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 1 and height > 1:  # Avoid division by zero or negative value
            # Adjust title size and position
            title_font_size = max(16, min(20, int(width / 40)))  
            self.title_label.config(font=("Comic Sans MS", title_font_size, "bold"))
            
            # Adjust frame sizes proportionally
            # For smaller screens, make frames stack vertically
            if width < 800:
                # Move to vertical layout
                self.input_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
                self.summary_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
                self.savings_summary_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
                self.table_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
                self.button_frame.grid(row=6, column=0, columnspan=3, pady=20, sticky="n")
            else:
                # Restore horizontal layout
                self.input_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
                self.summary_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
                self.savings_summary_frame.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")
                self.table_frame.grid(row=3, column=0, columnspan=3, padx=30, pady=(30, 10), sticky="nsew")
                self.button_frame.grid(row=5, column=0, columnspan=3, pady=20, sticky="n")