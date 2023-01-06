from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import file_renamer as fr


def select_folder():
    global target_path
    path_select = filedialog.askdirectory()
    target_path.set(path_select)
    target_path_text.delete(1.0, END)
    target_path_text.insert(1.0, path_select)


def add_replacement_key():
    replacement_keys.append(StringVar())
    key_entry = ttk.Entry(
        replacement_frame, textvariable=replacement_keys[-1], width=15).grid(
        column=0, row=len(replacement_keys)+1, pady=4)
    replacement_keys_entries.append(key_entry)


def add_replacement_value():
    replacement_values.append(StringVar())
    ttk.Entry(
        replacement_frame,
        textvariable=replacement_values[-1], width=15).grid(
            column=1, row=len(replacement_values)+1, pady=4, padx=12)


def set_replacements():
    # build replacements dictionary from user input
    for key, value in zip(replacement_keys, replacement_values):
        key = key.get()
        value = value.get()
        fr.replacements[key] = value


def apply_rename():
    set_replacements()
    fr.run_renamer(target_path.get())


# these hold the StringVars that will comprise the key/value pairs for
# 'replacements' dictionary in 'file_renamer.py'
replacement_keys = []
replacement_values = []
replacement_keys_entries = []
replacement_values_entries = []


root = Tk()
root.title("File Renamer")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0)

# target folder
target_path = StringVar()
target_path_text = Text(mainframe, height=1, width=50)
target_path_text.grid(column=0, row=1, padx=(12, 0))
target_path_label = ttk.Label(
    mainframe, text='1. Select target folder:').grid(
        sticky=W, column=0, row=0)
select_folder_btn = ttk.Button(
    mainframe, text="Browse", command=select_folder).grid(
        column=1, row=1, padx=(12, 0))

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

# replacement frame
replacement_frame = ttk.Frame(mainframe, padding=("10 0"))
replacement_frame.grid(sticky=W, column=0, row=6, pady=(12, 0))

# replacement rules
replacement_key_text = Text(mainframe, height=1, width=30)
replacement_label = ttk.Label(
    mainframe, text="3. Add replacement rules:").grid(
        sticky=W, column=0, row=5, pady=12)
replacement_key_label = ttk.Label(replacement_frame, text="Target:").grid(
    sticky=W, column=0, row=0)
replacement_value_label = ttk.Label(
    replacement_frame, text="Replacement:").grid(
        sticky=W, column=1, row=0, padx=12)

replacement_add_btn = ttk.Button(
    mainframe, text="Add",
    command=lambda: [add_replacement_key(), add_replacement_value()]).grid(
        column=0, row=5, padx=(24, 0))

# apply rename
apply_rename_btn = ttk.Button(
    mainframe, text="Apply", command=apply_rename).grid(
        sticky=SE, column=1, row=6)

add_replacement_key()
add_replacement_value()

root.mainloop()
