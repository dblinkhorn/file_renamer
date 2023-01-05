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
    replacement_entry = ttk.Entry(mainframe).grid(
        column=0, row=len(replacement_keys)+6)


# these hold the Entry widgets that will comprise the key/value pairs for
# 'replacements' dictionary in 'file_renamer.py'
replacement_keys = []
replacement_values = []


root = Tk()
root.title("File Renamer")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0)

# target folder
target_path = StringVar()
target_path_text = ttk.Entry(
    mainframe, textvariable=target_path, width=50)
target_path_text.grid(column=0, row=1, padx=(0, 12))
target_path_label = ttk.Label(
    mainframe,
    text='1. Select target folder:').grid(sticky=W, column=0, row=0)
select_folder_btn = ttk.Button(
    mainframe, text="Select Folder",
    command=select_folder).grid(column=1, row=1)

# force case
case_value = StringVar()
case_value.set(None)
lowercase_check = Radiobutton(
    mainframe, text=" Lowercase", variable=case_value,
    value="lowercase").grid(column=0, row=3, sticky=W)
lowercase_label = ttk.Label(mainframe, text="2. Force case (optional):").grid(
    sticky=W, column=0, row=2, pady=(12, 0))
uppercase_check = Radiobutton(
    mainframe, text=" Uppercase", variable=case_value,
    value="uppercase").grid(column=0, row=4, sticky=W)

# replacement rules
replacement_key_text = Text(mainframe, height=1, width=30)
replacement_label = ttk.Label(
    mainframe,
    text="3. Add replacement rules:").grid(sticky=W, column=0, row=5, pady=12)

# add_replacement_btn = ttk.Button(
# mainframe, text="Add", command=add_replacement).grid(column=0, row=4)

root.mainloop()
