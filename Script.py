import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ttkthemes import ThemedTk
import os
import json
import webbrowser
import os
import shutil
import requests

TESTworshopPath = 'E:/steam/steamapps/workshop/content/294100'
TESTjsonPath = 'mod_names.json'
TESTjsonPathWrong = 'mod_names copy.json'
TESTConfigPath = 'ExampleConfig'
TESTModlistsPath = 'ExampleModLists'


# ====================================================================================================================================================================
# Tool functions
# ====================================================================================================================================================================


# Function to get a modlist from a workshop folder
def GetModList_FromFolder(dir):
    file_names = os.listdir(dir)
    ModNames = []
    for file_name in file_names:
        ModNames.append(file_name)
    return ModNames
# Run example
# print(GetModList_FromFolder(TESTworshopPath))

# Function to get a modlist from a JsonFile folder
def GetModList_FromJson(dir):
    with open(dir, 'r') as json_file:
        ModNames = json.load(json_file)
    return ModNames
# Run example
# print(GetModList_FromJson(TESTjsonPath))

# Function to make a JsonFile from an array
def MakeJsonFile_FromArray(dir, array):
    with open(dir, 'w') as json_file:
        json.dump(array, json_file)
# Run example
# MakeJsonFile_FromArray(TESTjsonPath, GetModList_FromFolder(TESTworshopPath))

# Function to check if all elements in reference are present in compared
def check_elements_present(reference, compared):
    return all(element in compared for element in reference)
def get_extra_elements_in_compared(reference, compared):
    return list(set(reference) - set(compared))
# Run example
# print(get_extra_elements_in_compared(GetModList_FromFolder(TESTworshopPath), GetModList_FromJson(TESTjsonPathWrong)))
# print(get_extra_elements_in_compared(GetModList_FromJson(TESTjsonPathWrong), GetModList_FromFolder(TESTworshopPath)))

# Open a modpage in the steam workshop
def OpenModpage(modids):
    for modid in modids:
        url = 'https://steamcommunity.com/sharedfiles/filedetails/?id=' + str(modid)
        webbrowser.open(url)
# Run example
# OpenModpage(get_extra_elements_in_compared(GetModList_FromFolder(TESTworshopPath), GetModList_FromJson(TESTjsonPathWrong)))

# Function to check if a directory exists in any of the users drives
def check_directory_exists(path):
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in drives:
        directory_path = os.path.join(drive, path)
        if os.path.exists(directory_path):
            return directory_path
    return 'none'
# Run example
# directory_path = '/steam/steamapps/workshop/content/294100'
# print(check_directory_exists(directory_path))

def copy_folder_content(source_folder, destination_folder):
    shutil.rmtree(destination_folder)
    shutil.copytree(source_folder, destination_folder)
# Run example
# copy_folder_content("C:/Users/vpali/Desktop/ExampleConfig", "C:/Users/vpali/Desktop/testSync - Copie")

# Function to fetch mod names from Steam API
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

# ====================================================================================================================================================================
# Main functions
# ====================================================================================================================================================================


# Create a file containing any files necessary to sync mods
def CreateSyncFile(name, WorkshopFolderPath, ConfigFolderPath, ModlistsFolderPath):
    # Create the folder and subfolders
    os.mkdir(os.path.join(os.environ['USERPROFILE'], 'Desktop', name))
    os.mkdir(os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'config'))
    os.mkdir(os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'modlist'))
    os.mkdir(os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'mods'))
    
    # List of all mods in the workshop folder in Json Format in the sync folder
    ModList = GetModList_FromFolder(WorkshopFolderPath)
    MakeJsonFile_FromArray(os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'mods', 'modsID.json'), ModList)
    
    # Copy config folder to the sync folder
    copy_folder_content(ConfigFolderPath, os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'config'))
    
    # Copy modlist folder to the sync folder
    copy_folder_content(ModlistsFolderPath, os.path.join(os.environ['USERPROFILE'], 'Desktop', name, 'modlist'))
    
    return True
# Run example
#CreateSyncFile('test', TESTworshopPath, TESTConfigPath, TESTModlistsPath)

def Sync(SyncFolderPath, WorkshopFolderPath, ConfigFolderPath, ModlistsFolderPath):
    # Check if all the mods are present in the workshop folder
    ModListFromWorkshop = GetModList_FromFolder(WorkshopFolderPath)
    ModListFromSync = GetModList_FromJson(os.path.join(SyncFolderPath, 'mods', 'modsID.json'))
    if check_elements_present(ModListFromWorkshop, ModListFromSync):
        pass
    else:
        ModsToRemove = get_extra_elements_in_compared(ModListFromSync, ModListFromWorkshop)
        ModsToAdd = get_extra_elements_in_compared(ModListFromWorkshop, ModListFromSync)
        return False, ModsToRemove, ModsToAdd
    
    # Copy the config from sync to the game folder
    copy_folder_content(os.path.join(SyncFolderPath, 'config'), ConfigFolderPath)
    
    # Copy the modlist from sync to the game folder
    copy_folder_content(os.path.join(SyncFolderPath, 'modlist'), ModlistsFolderPath)
    
    return True


# ====================================================================================================================================================================
# Interface
# ====================================================================================================================================================================

# ==========================================
# General interface parameters
# ==========================================

# Create the interface
root = tk.Tk()
root.title("Rimworld Mod Sync")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size as a percentage of the screen dimensions
window_width = int(screen_width * 0.5)  # 50% of the screen width
window_height = int(screen_height * 0.5)  # 50% of the screen height
window_size = f"{window_width}x{window_height}"
root.geometry(window_size)

# Function when window closed
def close_sub_window():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close_sub_window)

style = ttk.Style()

style.configure("TButton",
                font=("Arial", 14),  # Increased font size for buttons
                padding=10)

style.configure("TLabel",
                font=("Arial", 14))  # Increased font size for labels

style.configure("TCheckbutton",
                font=("Arial", 14))  # Increased font size for check buttons

# ==========================================
# Functions for Creating a sync folder
# ==========================================

# Window to create a Sync Folder, automatically finding the workshop folder, config folder and modlist folder
def open_SyncFileAuto_window():
    root.attributes("-disabled", True)
    SyncFileAuto_window = tk.Toplevel(root)
    SyncFileAuto_window.title("Choose sync folder parameters")
    size = 100;
    
    name_label = ttk.Label(SyncFileAuto_window, text="Folder Name")
    name_entry = ttk.Entry(SyncFileAuto_window)
    name_label.pack(fill=tk.BOTH, expand=True)
    name_entry.pack(fill=tk.BOTH, expand=True)
    
    # Check workshop folder automatically or deflauts to manual input
    WorkshopFolderPath = check_directory_exists('/steam/steamapps/workshop/content/294100')
    if WorkshopFolderPath == 'none':
        Workshop_label = ttk.Label(SyncFileAuto_window, text="Workshop folder path")
        Workshop_entry = ttk.Entry(SyncFileAuto_window)
        Workshop_label.pack(fill=tk.BOTH, expand=True)
        Workshop_entry.pack(fill=tk.BOTH, expand=True)
        size = size + 75
    else:
        Workshop_entry = ttk.Entry(SyncFileAuto_window)
        Workshop_entry.insert(0, WorkshopFolderPath)
        
    # Check config folder automatically or deflauts to manual input
    user_profile = os.environ.get('USERPROFILE')
    ConfigFolderPath = os.path.join(user_profile, 'AppData', 'LocalLow', 'Ludeon Studios', 'RimWorld by Ludeon Studios', 'Config')
    if os.path.exists(ConfigFolderPath) == False:
        Config_label = ttk.Label(SyncFileAuto_window, text="Config folder path")
        Config_entry = ttk.Entry(SyncFileAuto_window)
        Config_label.pack(fill=tk.BOTH, expand=True)
        Config_entry.pack(fill=tk.BOTH, expand=True)
        size = size + 75
    else:
        Config_entry = ttk.Entry(SyncFileAuto_window)
        Config_entry.insert(0, ConfigFolderPath)
    
    # Check modlist folder automatically or deflauts to manual input
    user_profile = os.environ.get('USERPROFILE')
    ModlistsFolderPath = os.path.join(user_profile, 'AppData', 'LocalLow', 'Ludeon Studios', 'RimWorld by Ludeon Studios', 'ModLists')
    if os.path.exists(ModlistsFolderPath) == False:
        Modlist_label = ttk.Label(SyncFileAuto_window, text="ModLists folder path")
        Modlist_entry = ttk.Entry(SyncFileAuto_window)
        Modlist_label.pack(fill=tk.BOTH, expand=True)
        Modlist_entry.pack(fill=tk.BOTH, expand=True)
        size = size + 75
    else:
        Modlist_entry = ttk.Entry(SyncFileAuto_window)
        Modlist_entry.insert(0, ModlistsFolderPath)

    # Function to create the sync folder, checking if the paths are valid beforehand
    def create_sync_file():
        if os.path.exists(Workshop_entry.get()) and os.path.exists(Config_entry.get()) and os.path.exists(Modlist_entry.get()):
            CreateSyncFile(name_entry.get(), Workshop_entry.get(), Config_entry.get(), Modlist_entry.get())
            root.attributes("-disabled", False)
            SyncFileAuto_window.destroy()
        else:
            if not os.path.exists(Workshop_entry.get()):
                Workshop_label.config(text="Workshop folder path: does not exist")
            if not os.path.exists(Config_entry.get()):
                Config_label.config(text="Config folder path: does not exist")
            if not os.path.exists(Modlist_entry.get()):
                Modlist_label.config(text="ModLists folder path: does not exist")

    SyncFileAuto_window.geometry("500x" + str(size))
    
    create_sync_button = ttk.Button(SyncFileAuto_window, text="Create Sync File", command=create_sync_file)
    create_sync_button.pack(fill=tk.BOTH, expand=True)
    
    # Function to call when window closed
    def close_sub_window():
        SyncFileAuto_window.destroy()
        root.attributes("-disabled", False)
    SyncFileAuto_window.protocol("WM_DELETE_WINDOW", close_sub_window)

# Window to create a Sync Folder, manually inputting the workshop folder, config folder and modlist folder
def open_SyncFile_window():
    root.attributes("-disabled", True)
    SyncFile_window = tk.Toplevel(root)
    SyncFile_window.title("Choose sync folder parameters")
    SyncFile_window.geometry("500x325")
    
    name_label = ttk.Label(SyncFile_window, text="Folder Name")
    name_entry = ttk.Entry(SyncFile_window)
    name_label.pack(fill=tk.BOTH, expand=True)
    name_entry.pack(fill=tk.BOTH, expand=True)
    
    Workshop_label = ttk.Label(SyncFile_window, text="Workshop folder path")
    Workshop_entry = ttk.Entry(SyncFile_window)
    Workshop_label.pack(fill=tk.BOTH, expand=True)
    Workshop_entry.pack(fill=tk.BOTH, expand=True)
    
    Config_label = ttk.Label(SyncFile_window, text="Config folder path")
    Config_entry = ttk.Entry(SyncFile_window)
    Config_label.pack(fill=tk.BOTH, expand=True)
    Config_entry.pack(fill=tk.BOTH, expand=True)
    
    Modlist_label = ttk.Label(SyncFile_window, text="ModLists folder path")
    Modlist_entry = ttk.Entry(SyncFile_window)
    Modlist_label.pack(fill=tk.BOTH, expand=True)
    Modlist_entry.pack(fill=tk.BOTH, expand=True)
    
    # Function to create the sync folder, checking if the paths are valid beforehand
    def create_sync_file():
        if os.path.exists(Workshop_entry.get()) and os.path.exists(Config_entry.get()) and os.path.exists(Modlist_entry.get()):
            CreateSyncFile(name_entry.get(), Workshop_entry.get(), Config_entry.get(), Modlist_entry.get())
            root.attributes("-disabled", False)
            SyncFile_window.destroy()
        else:
            if not os.path.exists(Workshop_entry.get()):
                Workshop_label.config(text="Workshop folder path: does not exist")
            if not os.path.exists(Config_entry.get()):
                Config_label.config(text="Config folder path: does not exist")
            if not os.path.exists(Modlist_entry.get()):
                Modlist_label.config(text="ModLists folder path: does not exist")

    create_sync_button = ttk.Button(SyncFile_window, text="Create Sync File", command=create_sync_file)
    create_sync_button.pack(fill=tk.BOTH, expand=True)
    
    # Function to call when window closed
    def close_sub_window():
        SyncFile_window.destroy()
        root.attributes("-disabled", False)
    SyncFile_window.protocol("WM_DELETE_WINDOW", close_sub_window)

# ==========================================
# Functions for Importing a sync folder
# ==========================================

def open_Import_window(*args):
    root.attributes("-disabled", True)
    Import_window = tk.Toplevel(root)
    Import_window.title("Choose sync folder parameters")
    size = 100
    
    # User needs to input the path of the sync folder
    Folder_label = ttk.Label(Import_window, text="Folder Path")
    Folder_entry = ttk.Entry(Import_window)
    Folder_label.pack(fill=tk.BOTH, expand=True)
    Folder_entry.pack(fill=tk.BOTH, expand=True)
    
    # Function to create the sync folder, checking if the paths are valid beforehand
    def Sync_file():
        if os.path.exists(Workshop_entry.get()) and os.path.exists(Config_entry.get()) and os.path.exists(Modlist_entry.get()):
            Status = Sync(Folder_entry.get(), Workshop_entry.get(), Config_entry.get(), Modlist_entry.get())
            if Status == True:
                root.attributes("-disabled", False)
                Import_window.destroy()
            else:
                root.attributes("-disabled", False)
                Import_window.destroy()
                open_ModMismatch_window(Status[1], Status[2])
        else:
            if not os.path.exists(Workshop_entry.get()):
                Workshop_label.config(text="Workshop folder path: does not exist")
            if not os.path.exists(Config_entry.get()):
                Config_label.config(text="Config folder path: does not exist")
            if not os.path.exists(Modlist_entry.get()):
                Modlist_label.config(text="ModLists folder path: does not exist")
    
    # If Auto_Pathing is enabled, the paths are automatically found
    if Auto_Pathing.get():
        # Check workshop folder automatically or deflauts to manual input
        WorkshopFolderPath = check_directory_exists('/steam/steamapps/workshop/content/294100')
        if WorkshopFolderPath == 'none':
            Workshop_label = ttk.Label(Import_window, text="Workshop folder path")
            Workshop_entry = ttk.Entry(Import_window)
            Workshop_label.pack(fill=tk.BOTH, expand=True)
            Workshop_entry.pack(fill=tk.BOTH, expand=True)
            size = size + 75
        else:
            Workshop_entry = ttk.Entry(Import_window)
            Workshop_entry.insert(0, WorkshopFolderPath)
            
        # Check config folder automatically or deflauts to manual input
        user_profile = os.environ.get('USERPROFILE')
        ConfigFolderPath = os.path.join(user_profile, 'AppData', 'LocalLow', 'Ludeon Studios', 'RimWorld by Ludeon Studios', 'Config')
        if os.path.exists(ConfigFolderPath) == False:
            Config_label = ttk.Label(Import_window, text="Config folder path")
            Config_entry = ttk.Entry(Import_window)
            Config_label.pack(fill=tk.BOTH, expand=True)
            Config_entry.pack(fill=tk.BOTH, expand=True)
            size = size + 75
        else:
            Config_entry = ttk.Entry(Import_window)
            Config_entry.insert(0, ConfigFolderPath)
            
        # Check modlist folder automatically or deflauts to manual input
        user_profile = os.environ.get('USERPROFILE')
        ModlistsFolderPath = os.path.join(user_profile, 'AppData', 'LocalLow', 'Ludeon Studios', 'RimWorld by Ludeon Studios', 'ModLists')
        if os.path.exists(ModlistsFolderPath) == False:
            Modlist_label = ttk.Label(Import_window, text="ModLists folder path")
            Modlist_entry = ttk.Entry(Import_window)
            Modlist_label.pack(fill=tk.BOTH, expand=True)
            Modlist_entry.pack(fill=tk.BOTH, expand=True)
            size = size + 75
        else:
            Modlist_entry = ttk.Entry(Import_window)
            Modlist_entry.insert(0, ModlistsFolderPath)
    # If Auto_Pathing is disabled, the user needs to input the paths
    else:
        Workshop_label = ttk.Label(Import_window, text="Workshop folder path")
        Workshop_entry = ttk.Entry(Import_window)
        Workshop_label.pack(fill=tk.BOTH, expand=True)
        Workshop_entry.pack(fill=tk.BOTH, expand=True)
        
        Config_label = ttk.Label(Import_window, text="Config folder path")
        Config_entry = ttk.Entry(Import_window)
        Config_label.pack(fill=tk.BOTH, expand=True)
        Config_entry.pack(fill=tk.BOTH, expand=True)
        
        Modlist_label = ttk.Label(Import_window, text="ModLists folder path")
        Modlist_entry = ttk.Entry(Import_window)
        Modlist_label.pack(fill=tk.BOTH, expand=True)
        Modlist_entry.pack(fill=tk.BOTH, expand=True)
        size = size + 225

    Import_window.geometry("500x" + str(size))
    
    Sync_button = ttk.Button(Import_window, text="Sync", command=Sync_file)
    Sync_button.pack(fill=tk.BOTH, expand=True)
    
    def close_sub_window():
        Import_window.destroy()
        root.attributes("-disabled", False)
    Import_window.protocol("WM_DELETE_WINDOW", close_sub_window)

# ==========================================
# Mod mismatch window
# ==========================================

def open_ModMismatch_window(ModsToAdd, ModsToRemove):
    root.attributes("-disabled", True)
    ModMismatch_window = tk.Toplevel(root)
    ModMismatch_window.title("Choose sync folder parameters")
    ModMismatch_window.geometry("500x400")
    
    def call_Modpage_Add():
        OpenModpage(ModsToAdd)
        
    def call_Modpage_Remove():
        OpenModpage(ModsToRemove)
    
    add_label = ttk.Label(ModMismatch_window, text="Mods to add:")
    add_label.pack(fill=tk.BOTH, expand=True)
    
    add_scroll = scrolledtext.ScrolledText(ModMismatch_window, width=40, height=5)
    add_scroll.pack(fill=tk.BOTH, expand=True)
    for mod in ModsToAdd:
        add_scroll.insert(tk.END, get_mod_name(mod) + '\n')
    add_scroll.configure(state='disabled')  # Disable editing

    
    Link_Add_button = ttk.Button(ModMismatch_window, text="Open Modpage (Add)", command=call_Modpage_Add)
    Link_Add_button.pack(fill=tk.BOTH, expand=True)
    
    remove_label = ttk.Label(ModMismatch_window, text="Mods to remove:")
    remove_label.pack(fill=tk.BOTH, expand=True)
    
    remove_scroll = scrolledtext.ScrolledText(ModMismatch_window, width=40, height=5)
    remove_scroll.pack(fill=tk.BOTH, expand=True)
    for mod in ModsToRemove:
        remove_scroll.insert(tk.END, get_mod_name(mod) + '\n')
    remove_scroll.configure(state='disabled')  # Disable editing
    
    Link_Remove_button = ttk.Button(ModMismatch_window, text="Open Modpage (Remove)", command=call_Modpage_Remove)
    Link_Remove_button.pack(fill=tk.BOTH, expand=True)
    
    def close_sub_window():
        ModMismatch_window.destroy()
        root.attributes("-disabled", False)
        
    ModMismatch_window.protocol("WM_DELETE_WINDOW", close_sub_window)

# ==========================================
# Choose Auto or Manual pathing for Sync
# ==========================================

# Create a BooleanVar to store the selected value of the Checkbox
Auto_Pathing = tk.BooleanVar()
Auto_Pathing.set(True)

# Define a function to handle the visibility change
def handle_visibility_change(*args):
    visibility = Auto_Pathing.get()
    if visibility:
        Sync_button_auto.pack(fill=tk.BOTH, expand=True)
        Sync_button_manual.pack_forget()
    else:
        Sync_button_manual.pack(fill=tk.BOTH, expand=True)
        Sync_button_auto.pack_forget()

# Create the checkbox
visibility_checkbox = ttk.Checkbutton(root, text="Auto Pathing", variable=Auto_Pathing, onvalue=True, offvalue=False)
visibility_checkbox.pack()

# Call the handle_visibility_change function when the checkbox value changes
Auto_Pathing.trace_add("write", handle_visibility_change)

# Create the buttons
Import_button = ttk.Button(root, text="Import Sync Folder", command=open_Import_window)
Import_button.pack(fill=tk.BOTH, expand=True)

Sync_button_auto = ttk.Button(root, text="Generate Sync Folder", command=open_SyncFileAuto_window)
Sync_button_manual = ttk.Button(root, text="Generate Sync Folder", command=open_SyncFile_window)
Sync_button_auto.pack(fill=tk.BOTH, expand=True)

# Run the interface
root.mainloop()
