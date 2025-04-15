import tkinter as tk 

class LoginFrame(tk.Frame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create and place background canvas
        self.canvas = tk.Canvas(self, width = 800, height = 600, highlightthickness=0, bg="#f1e7e7")
        self.canvas.pack(fill = "both", expand = True)

        self.canvas.create_text(
            400, 180, 
            text="Login Page", 
            font=("Comic Sans MS", 16), 
            fill="#333333"
        )