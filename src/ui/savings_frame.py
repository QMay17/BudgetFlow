import tkinter as tk
from tkinter import ttk, messagebox
from src.models.savings import save_saving, load_all_savings
from src.models.database import get_savings_db_connection as get_db_connection



class SavingsFrame(tk.Frame):
    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.transactions = []  # to store all transactions
        self.total_savings = 0
        self.saving_categories = {
            "Living savings": 0,
            "Transportation": 0,
            "Healthcare": 0,
            "Groceries": 0,
            "Personal spending": 0,
            "Recreation": 0
        }
        self.total_income = 4000  # Default income value
        self.income_types = ["Paycheck", "Investment", "Scholarships", "Bonuses", "Others"]

        # Main background
        self.configure(bg="#f5efef")
        
        # Title text
        self.title_label = tk.Label(
            self,
            text="Savings Tracker",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f5efef",
            fg="#333333"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(15, 20), sticky="n")

        # Create frames
        self.create_income_header()
        self.create_input_section()
        self.create_summary_section()
        self.create_transaction_table()
        self.create_navigation_buttons()

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

        # Add these styles for the Combobox
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
        
        # Changed black background to white with black text
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
        # Left section - saving input
        self.input_frame = tk.Frame(self, bg="#ffdddd", padx=20, pady=20, relief="flat")
        self.input_frame.grid(row=2, column=0, padx=30, pady=10, sticky="n")
        
        # Input section title
        input_title = tk.Label(
            self.input_frame, 
            text="Enter your savings here...",
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
        # For the category dropdown (in create_input_section method)
        # Replace the existing style with this:
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff")
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        
        self.category_dropdown = ttk.Combobox(
            self.input_frame,
            font=("Comic Sans MS", 12),
            values=list(self.saving_categories.keys()),
            width=22
        )
        self.category_dropdown.set("Living savings")
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
        self.add_button.grid(row=4, column=1, pady=15, sticky="e")

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
        self.summary_frame.grid(row=2, column=1, padx=20, pady=10, sticky="n")
        
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
        
        # Create labels for each saving category
        for category in self.saving_categories:
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
            self.saving_categories[category] = label
        
        # Separator
        separator = tk.Frame(self.summary_frame, height=2, bg="#ffb3b3")
        separator.pack(fill="x", pady=8)
        
        # Total savings
        self.total_container = tk.Frame(self.summary_frame, bg="#ffb3b3")
        self.total_container.pack(fill="x", pady=2)
        
        tk.Label(
            self.total_container,
            text="Total savings ...",
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

    def create_transaction_table(self):
        # savings table
        self.table_frame = tk.Frame(self, bg="#f5efef")
        self.table_frame.grid(row=3, column=0, columnspan=2, padx=30, pady=(30, 10), sticky="ew")
        
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
        
        # For the scrollbar (in create_transaction_table method)
        # Replace the existing scrollbar setup with this:
        scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.transaction_table.yview)
        self.transaction_table.configure(yscrollcommand=scrollbar.set)

        # Add this style configuration for the scrollbar
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", background="white", arrowcolor="black", 
                        troughcolor="white", bordercolor="white")
        scrollbar.configure(style="Vertical.TScrollbar")
        
        # Set up columns
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
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
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
            text="Done",
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
            self.income_value.config(text=f"${self.total_income:.2f}")
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
            
            # Add to transaction table
            self.transaction_table.insert("", tk.END, values=(income_type, f"${amount:.2f}", "Income"))
            
            # Save to database
            save_saving(income_type, amount, "Income")
            
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
        
        # For compatibility with your existing code
        trans_type = "Saving"
        
        # Store in memory
        self.transactions.append({
            "name": name,
            "category": category,
            "amount": amount,
            "type": trans_type
        })
        
        # Save to database (using your existing function)
        save_saving(category, amount, trans_type)
        
        # Insert into table
        self.transaction_table.insert("", tk.END, values=(category, f"${amount:.2f}", trans_type))
        
        # Update summary
        self.update_summary(category, amount)
        
        # Reset inputs
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.set("Living savings")
        
        messagebox.showinfo("Success", f"Added ${amount:.2f} to {category}")

    def update_summary(self, category, amount):
        # Update category amount
        if category in self.saving_categories:
            current_text = self.saving_categories[category].cget("text")
            current_amount = float(current_text.replace("$", ""))
            new_amount = current_amount + amount
            self.saving_categories[category].config(text=f"${new_amount:.2f}")
            
            # Update total
            self.total_savings += amount
            self.total_value.config(text=f"${self.total_savings:.2f}")

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

        # Delete from DB (keeping your original code)
        
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

        # Update summary (subtract the amount)
        if trans_type == "Saving" and category in self.saving_categories:
            current_text = self.saving_categories[category].cget("text")
            current_amount = float(current_text.replace("$", ""))
            new_amount = current_amount - amount
            self.saving_categories[category].config(text=f"${new_amount:.2f}")
            
            # Update total
            self.total_savings -= amount
            self.total_value.config(text=f"${self.total_savings:.2f}")
        elif trans_type == "Income":
            # Update total income
            self.total_income -= amount
            self.income_value.config(text=f"${self.total_income:.2f}")

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

        # If it's a saving
        if trans_type == "Saving":
            # Update summary (subtract the amount first since we're editing)
            if category in self.saving_categories:
                current_text = self.saving_categories[category].cget("text")
                current_amount = float(current_text.replace("$", ""))
                new_amount = current_amount - amount
                self.saving_categories[category].config(text=f"${new_amount:.2f}")
                
                # Update total
                self.total -= amount
                self.total_value.config(text=f"${self.total_expenses:.2f}")

            # Pre-fill inputs
            self.category_dropdown.set(category)
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, amount_text.strip("$"))
        # If it's income
        elif trans_type == "Income":
            # Update total income
            self.total_income -= amount
            self.income_value.config(text=f"${self.total_income:.2f}")
            
            # Pre-fill income inputs
            if category in self.income_types:
                self.income_type.set(category)
            self.income_entry.delete(0, tk.END)
            self.income_entry.insert(0, amount_text.strip("$"))

        # Remove original entry from table and DB
        self.transaction_table.delete(selected[0])

        
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
        messagebox.showinfo("Done", "All transactions saved!")
        self.controller.show_frame("profile")