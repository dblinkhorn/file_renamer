from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import file_renamer as fr


def select_folder():
    global target_path
    selected_path = filedialog.askdirectory()
    target_path.set(selected_path)
    target_path_text.delete(1.0, END)
    target_path_text.insert(1.0, selected_path)


def add_replacement_key():
    replacement_keys.append(StringVar())
    # entry value will be bound to the StringVar appended above
    ttk.Entry(
        replacement_frame, textvariable=replacement_keys[-1], width=15).grid(
        column=0, row=len(replacement_keys)+1, pady=4)


def add_replacement_value():
    replacement_values.append(StringVar())
    ttk.Entry(
        replacement_frame,
        textvariable=replacement_values[-1], width=15).grid(
            column=1, row=len(replacement_values)+1, pady=4, padx=12)


def set_case():
    if case_value.get() == 'lowercase':
        fr.lowercase = True
    if case_value.get() == 'uppercase':
        fr.uppercase = True


def set_replacements():
    # build replacements dictionary from user input
    for key, value in zip(replacement_keys, replacement_values):
        key = key.get()
        value = value.get()
        fr.replacements[key] = value


def apply_rename():
    set_case()
    set_replacements()
    fr.run_renamer(target_path)


def confirm_rename():
    modal_root = Tk()
    modal_root.attributes('-topmost', True)
    modal_root.title("Confirm Rename")
    modal_frame = ttk.Frame(
        modal_root, padding="12 12 12 12")
    modal_frame.grid(column=0, row=0)
    if not target_path.get():
        empty_path_msg = "You must specify a valid target directory. Please try again."
        ttk.Label(modal_frame, text=empty_path_msg).grid(column=0, row=1)
        ttk.Button(
            modal_frame, text="Okay", command=modal_root.destroy).grid(
                sticky=E, column=0, row=2, pady=(12, 0))
        return
    # get total files & dirs that will be inspected
    file_count, dir_count = fr.get_counts(target_path.get())
    no_files_msg = '\nNo files found. Please select another directory.'
    if file_count > 0:
        singular_subdir_string = 'sub-directory'
        plural_subdir_string = 'sub-directories'
        # determine singular or plural
        subdir_string = (singular_subdir_string if dir_count == 1
                         else plural_subdir_string)
        subdirs_string = f', including {dir_count} {subdir_string},'
        count_string = (f'\n{file_count} files'
                        f'{subdirs_string if dir_count else ""} '
                        'will be affected.\n')
        files_msg = count_string if file_count else no_files_msg
        # this will be rendered on the confirm modal
        confirm_message = (f'\nSelected target directory: {target_path.get()}'
                           f'\n{files_msg}'
                           '\nAre you sure you wish to proceed '
                           'with this rename operation?')
        ttk.Label(modal_frame, text=confirm_message).grid(
            column=0, row=1, pady=(0, 12))
        ttk.Button(
            modal_frame, text="Confirm",
            command=lambda: [apply_rename(), modal_root.destroy()]).grid(
                sticky=E, column=0, row=2)
        ttk.Button(
            modal_frame, text="Cancel", command=modal_root.destroy).grid(
                sticky=E, column=1, row=2, padx=(12, 0))
    else:
        ttk.Label(modal_frame, text=no_files_msg).grid(column=0, row=1)
        ttk.Button(
            modal_frame, text="Okay", command=modal_root.destroy).grid(
                sticky=E, column=0, row=2, pady=(12, 0))


# these hold the StringVars that will comprise the key/value pairs for
# 'replacements' dictionary in 'file_renamer.py'
replacement_keys = []
replacement_values = []

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
    mainframe, text="Apply", command=confirm_rename).grid(
        sticky=SE, column=1, row=6)

add_replacement_key()
add_replacement_value()

root.mainloop()
