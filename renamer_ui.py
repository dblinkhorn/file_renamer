from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import file_renamer


def select_folder():
    global target_path
    path_select = filedialog.askdirectory()
    target_path.set(path_select)
    target_path_text.delete(1.0, END)
    target_path_text.insert(1.0, path_select)


def add_replacement():
    replacement_keys.append(StringVar())
    replacement_entry = Entry(mainframe).grid(
        column=0, row=len(replacement_keys)+1)


# these hold the Entry widgets that will comprise the key/value pairs for
# 'replacements' dictionary in 'file_renamer.py'
replacement_keys = []
replacement_values = []


root = Tk()
root.title("File Renamer")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0)

target_path = StringVar()
target_path_text = Text(mainframe, height=1, width=50).grid(column=0, row=0)

add_replacement_btn = ttk.Button(
    mainframe, text="Add", command=add_replacement).grid(column=0, row=1)

select_folder_btn = ttk.Button(
    mainframe, text="Select Folder",
    command=select_folder).grid(column=1, row=0)

root.mainloop()
