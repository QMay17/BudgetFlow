import tkinter as tk

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller

        # Background
        self.canvas = tk.Canvas(self, bg="#f1e7e7")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            400, 250,
            text="Profile Summary Page (Coming Soon)",
            font=("Comic Sans MS", 20, "bold"),
            fill="#333333"
        )

        # Back to Welcome (just to test navigation)
        back_btn = tk.Button(
            self,
            text="Back to Welcome",
            font=("Comic Sans MS", 12),
            bg="#fffece",
            command=lambda: controller.show_frame("welcome")
        )
        self.canvas.create_window(400, 350, window=back_btn)
