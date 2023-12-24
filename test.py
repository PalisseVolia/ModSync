import tkinter as tk
from tkinter import scrolledtext
import requests

# Function to fetch mod names from Steam API
import json

import json

def get_mod_name(mod_id):
    url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"itemcount": "1", "publishedfileids[0]": str(mod_id)}
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("response", {}).get("result", 0) == 1:
                return data["response"]["publishedfiledetails"][0]["title"]
    except Exception as e:
        print(f"Error fetching mod details: {e}")
    
    return f"Mod ID {mod_id}"





# Your modified function
def open_ModMismatch_window(ModsToAdd, ModsToRemove):
    root = tk.Tk()  # Creating a root window for testing purposes
    root.geometry("600x400")

    def call_Modpage_Add():
        pass

    def call_Modpage_Remove():
        pass

    ModMismatch_window = tk.Toplevel(root)
    ModMismatch_window.title("Choose sync folder parameters")
    ModMismatch_window.geometry("500x400")

    add_label = tk.Label(ModMismatch_window, text="Mods to add:")
    add_label.pack()

    add_scroll = scrolledtext.ScrolledText(ModMismatch_window, width=40, height=5)
    add_scroll.pack()
    for mod in ModsToAdd:
        mod_name = get_mod_name(mod)
        add_scroll.insert(tk.END, mod_name + '\n')
    add_scroll.configure(state='disabled')  # Disable editing

    Link_Add_button = tk.Button(ModMismatch_window, text="Open Modpage (Add)", command=call_Modpage_Add)
    Link_Add_button.pack()

    remove_label = tk.Label(ModMismatch_window, text="Mods to remove:")
    remove_label.pack()

    remove_scroll = scrolledtext.ScrolledText(ModMismatch_window, width=40, height=5)
    remove_scroll.pack()
    for mod in ModsToRemove:
        mod_name = get_mod_name(mod)
        remove_scroll.insert(tk.END, mod_name + '\n')
    remove_scroll.configure(state='disabled')  # Disable editing

    Link_Remove_button = tk.Button(ModMismatch_window, text="Open Modpage (Remove)", command=call_Modpage_Remove)
    Link_Remove_button.pack()

    def close_sub_window():
        ModMismatch_window.destroy()
        root.destroy()

    ModMismatch_window.protocol("WM_DELETE_WINDOW", close_sub_window)
    root.mainloop()

# Test data (mock IDs)
ModsToAdd = [12345, 67890]
ModsToRemove = [54321, 98765]

# Call the function with test data
open_ModMismatch_window(ModsToAdd, ModsToRemove)
