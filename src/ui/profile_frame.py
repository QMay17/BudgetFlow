import tkinter as tk

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller

        # Background
        self.canvas = tk.Canvas(self, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            400, 150,
            text="Profile Summary Page (Coming Soon)",
            font=("Comic Sans MS", 20, "bold"),
            fill="#333333"
        )

        # Buttons container
        button_frame = tk.Frame(self, bg="#f1e7e7")
        self.canvas.create_window(400, 300, window=button_frame)

        # Manage Transactions Button
        tk.Button(
            button_frame,
            text="Manage Transactions",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("transaction")
        ).pack(pady=5)

        # Go to Savings Goal Tracker
        tk.Button(
            button_frame,
            text="Go to Savings Goal Tracker",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("savings")
        ).pack(pady=5)

        # Logout Button
        tk.Button(
            button_frame,
            text="Logout",
            font=("Comic Sans MS", 12),
            bg="#ffcccc",
            command=self.logout
        ).pack(pady=10)

    def logout(self):
        self.controller.auth_controller.handle_logout()
