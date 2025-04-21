import tkinter as tk
from tkinter import ttk, messagebox
from src.models.transaction import save_transaction


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

        # --------- Transaction Table (with scrollbar) ---------
        self.table_frame = tk.Frame(self.canvas, bg="#f1e7e7")
        self.canvas.create_window(400, 360, window=self.table_frame, anchor="n")

        columns = ("Category", "Amount", "Type")

        self.tree_container = tk.Frame(self.table_frame, bg="#f1e7e7")
        self.tree_container.pack()

        self.transaction_table = ttk.Treeview(
            self.tree_container,
            columns=columns,
            show="headings",
            height=6
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.transaction_table.yview)
        self.transaction_table.configure(yscrollcommand=scrollbar.set)

        self.transaction_table.pack(side="left")
        scrollbar.pack(side="right", fill="y")

        for col in columns:
            self.transaction_table.heading(col, text=col)
            self.transaction_table.column(col, anchor="center", width=140)

        # 💡 Right-click instruction label (outside table)
        tip_label = tk.Label(self.table_frame,
            text="💡 Right-click a transaction row to edit or delete it.",
            font=("Comic Sans MS", 10),
            bg="#f1e7e7",
            fg="#444"
        )
        tip_label.pack(pady=(5, 10))

                

        # --- Right-click menu ---
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)

        # Bind right-click to Treeview
        self.transaction_table.bind("<Button-3>", self.show_context_menu)


        # --------- Back Button ---------
        tk.Button(self.canvas, text="Back to Profile", font=("Comic Sans MS", 12), bg="#fffece",
                  command=lambda: controller.show_frame("profile")).place(x=320, y=580)
        
        # Done adding transactions button
        tk.Button(self.canvas, text="Done", font=("Comic Sans MS", 12), bg="#d4fcd4",
          command=self.finish_session).place(x=440, y=580)


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

        # Save to database (for both Saving and Expense)
        save_transaction(category, amount, trans_type)
        messagebox.showinfo("Success", f"Saved ${amount:.2f} to {category} as {trans_type}")


        # Insert into table
        self.transaction_table.insert("", tk.END, values=(category, f"${amount:.2f}", trans_type))

        # Reset inputs
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.set("Savings")
        self.type_dropdown.set("Saving")


    def show_context_menu(self, event):
    # Select the row under mouse before showing menu
        item_id = self.transaction_table.identify_row(event.y)
        if item_id:
            self.transaction_table.selection_set(item_id)
            self.context_menu.post(event.x_root, event.y_root)


    #deleting and editing transactions 

    #deleting 
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
        from src.models.database import get_db_connection
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

        # Delete from table
        self.transaction_table.delete(selected[0])
        messagebox.showinfo("Deleted", "Transaction deleted.")

    #edits transactions by deleting first and modifying 
    def edit_selected(self):
        selected = self.transaction_table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a transaction to edit.")
            return

        item = self.transaction_table.item(selected[0])
        values = item['values']
        category, amount_text, trans_type = values

        # Pre-fill inputs
        self.category_dropdown.set(category)
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, amount_text.strip("$"))
        self.type_dropdown.set(trans_type)

        # Remove original entry from table and DB (optional)
        self.transaction_table.delete(selected[0])

        from src.models.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM transactions 
        WHERE rowid = (
            SELECT rowid FROM transactions 
            WHERE category=? AND amount=? AND type=?
            LIMIT 1
        )
    """, (category, float(amount_text.strip("$")), trans_type))
        conn.commit()
        conn.close()

        messagebox.showinfo("Edit Mode", "Now modify the inputs and click 'Add Transaction' to re-save.")



    def finish_session(self):
        messagebox.showinfo("Done", "All transactions saved!")
        self.controller.show_frame("profile")

    