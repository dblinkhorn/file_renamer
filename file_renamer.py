# !/usr/bin/python

import os
from datetime import datetime

current_time = datetime.now()

# specify path to root folder
target_path = "/home/example-user/example-folder"

# specify substring replacements
replacements = {
    # target: replacement
    '%20': '_',
    ' ': '_',
}

renamed_count = 0
renamed_files = []


def get_counts(target_path):
    file_count = 0
    dir_count = 0  # does not include target_path dir

    for _, dirs, files in os.walk(target_path):
        file_count += len(files)
        dir_count += len(dirs)

    return [file_count, dir_count]


def set_confirmation(target_path):
    file_count, dir_count = get_counts(target_path)

    print(f'\nSelected root folder: {target_path}')
    count_string = f'{file_count} files, including {dir_count} sub-directories, will be affected...\n'

    if (file_count):
        print(count_string)
    else:
        return print('\nOperation aborted: No files found.')

    confirm_string = 'Are you sure you wish to proceed with rename operation? (y/n): '
    confirm_rename = input(confirm_string)

    return confirm_rename.lower() == 'y' or confirm_rename.lower() == 'yes'


def perform_rename(file, root):
    # save original filename
    original_filename = file

    # set original file path
    original_path = os.path.join(root, file)

    # replace substrings
    for substring, replacement in replacements.items():
        if substring in file:
            file = file.replace(substring, replacement)

            # force lowercase
            # file = file.lower()

            # force uppercase
            # file = file.upper()

    # set new file path
    new_path = os.path.join(root, file)

    # output processing if file name was changed
    if original_path != new_path:
        global renamed_count
        renamed_count += 1

        # rename file
        os.rename(original_path, new_path)

        output_string = f"'{original_filename}' --> '{file}'"
        renamed_files.append(output_string)
        print(output_string)


def rename_files(target_path):
    is_confirmed = set_confirmation(target_path)

    if (is_confirmed):
        for root, _, files in os.walk(target_path):
            for file in files:
                perform_rename(file, root)

        completed_string = f'\nOperation completed: {renamed_count} total files were renamed.'
        print(completed_string)

        # log results
        with open(f'{current_time}.txt', 'a') as log:
            log.write(f'Rename operation completed at {current_time}')
            log.write(f'\n{renamed_count} total files were renamed.\n\n')
            log.write('\n'.join(renamed_files))

    else:
        print('\nOperation aborted: Failed to confirm.')


get_counts(target_path)
rename_files(target_path)
