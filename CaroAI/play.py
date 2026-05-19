import tkinter as tk
from gui.interface import GomokuApp

if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuApp(root)
    root.mainloop()