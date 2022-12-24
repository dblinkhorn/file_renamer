# !/usr/bin/python

import os

# specify path to folder
target_path = "/home/dblinkhorn/Downloads/convert-folder"

# output colors
yellow = '\u001b[33m'
green = '\u001b[32m'
reset = '\u001b[0m'

for root, dirs, files in os.walk(target_path):
    for name in files:
        # save original name
        original_name = name

        # set original file path
        original_path = os.path.join(root, name)

        # specify character/substring replacements
        replacements = {
            ' - ': '-',
            ' -': '-',
            ' _ ': '-',
            '!': '',
            "'": '',
            ' ': '-',
        }

        # replace characters/substrings
        for substring, replacement in replacements.items():
            if substring in name:
                name = name.replace(substring, replacement)

                # force lowercase
                # name = name.lower()

                # force uppercase
                # name = name.upper()

        # set new file path
        new_path = os.path.join(root, name)

        # rename file
        os.rename(original_path, new_path)

        # output processing if file name was changed
        if original_path != new_path:
            output_string = f"{yellow}'{original_name}'{reset} >>> {green}'{name}'{reset}"
            print(output_string)
