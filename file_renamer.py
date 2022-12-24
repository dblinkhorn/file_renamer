# !/usr/bin/python

import os

# specify path to root folder
target_path = "/home/example-user/example-folder"

# specify substring replacements
replacements = {
    # target: replacement
    ' - ': '-',
    ' -': '-',
    ' _ ': '-',
    '%20': '-',
    '!': '',
    "'": '',
    ' ': '-',
}

# operation output colors
yellow = '\u001b[33m'
green = '\u001b[32m'
reset = '\u001b[0m'


def rename_files(target_path, replacements):
    print(f'Selected root folder: {target_path}\n')
    print('Replacement rules: ')
    for substring, replacement in replacements.items():
        print(f"'{substring}' will become '{replacement}'")

    confirm_string = 'Are you sure you wish to proceed with rename operation? (y/n): '
    confirm_rename = input(confirm_string)

    is_confirmed = confirm_rename.lower() == 'y' or confirm_rename.lower() == 'yes'

    if (is_confirmed):
        for root, dirs, files in os.walk(target_path):
            for dir in dirs:
                for name in files:
                    # save original name
                    original_name = name

                    # set original file path
                    original_path = os.path.join(root, name)

                    # replace substrings
                    for substring, replacement in replacements.items():
                        if substring in name:
                            name = name.replace(substring, replacement)

                            # force lowercase
                            # name = name.lower()

                            # force uppercase
                            # name = name.upper()

                    # set new file path
                    new_path = os.path.join(root, name)

                    # output processing if file name was changed
                    if original_path != new_path:
                        # rename file
                        os.rename(original_path, new_path)

                        output_string = f"{yellow}'{original_name}'{reset} >>> {green}'{name}'{reset}"
                        print(output_string)


rename_files(target_path, replacements)
