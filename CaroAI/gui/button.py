import tkinter as tk

def create_action_button(parent, text, bg, fg, command):
    """Hàm bổ trợ khởi tạo Button đồng nhất giao diện phong cách Dark Mode."""
    btn = tk.Button(
        parent, 
        text=text, 
        bg=bg, 
        fg=fg, 
        activebackground=bg,
        activeforeground=fg,
        font=("Arial", 10, "bold"), 
        command=command,
        relief=tk.RAISED,
        bd=2
    )
    return btn