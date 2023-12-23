import tkinter as tk
from tkinter import ttk

def open_SubWindow():
    sub_window = tk.Toplevel(root)
    sub_window.title("Sub Window")
    sub_window.geometry("300x200")

    def close_sub_window():
        sub_window.destroy()
        root.config(cursor="")
        root.attributes("-disabled", False)

    sub_window.protocol("WM_DELETE_WINDOW", close_sub_window)  # Bind closing event
    close_button = ttk.Button(sub_window, text="Close", command=close_sub_window)
    close_button.pack()

    # Disable interactions with the root window
    root.attributes("-disabled", True)
    root.config(cursor="watch")

root = tk.Tk()

def open_window_and_freeze():
    open_SubWindow()

open_window_button = ttk.Button(root, text="Open SubWindow", command=open_window_and_freeze)
open_window_button.pack()

root.mainloop()
