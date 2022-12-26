# !/usr/bin/python

import os
import sys
from datetime import datetime


# [ USER OPTIONS ] ************************************************************

# specify path to root folder
target_path = "/home/example-user/example-folder"

# specify substring replacements
replacements = {
    # target: replacement
    '%20': '_',
    ' ': '_',
}

# change either values below to True to force desired case, but not both
# only affects files that include a defined substring in 'replacements'
lowercase = False
uppercase = False

# *****************************************************************************

renamed_count = 0
renamed_files = []


def get_counts(target_path):
    file_count = 0
    dir_count = 0  # count does not include 'target_path' directory

    for _, dirs, files in os.walk(target_path):
        file_count += len(files)
        dir_count += len(dirs)

    return [file_count, dir_count]


def set_confirmation(target_path):
    file_count, dir_count = get_counts(target_path)

    print(f'\nSelected root folder: {target_path}')
    subdirs_string = f', including {dir_count} sub-directories,'
    count_string = f'\n{file_count} files{subdirs_string if dir_count else ""} will be affected...\n'

    if file_count:
        print(count_string)
    else:
        print('\nOperation aborted: No files found.')
        sys.exit()

    confirm_string = 'Are you sure you wish to proceed with rename operation? (y/n): '
    confirm_rename = input(confirm_string)

    return confirm_rename.lower() == 'y' or confirm_rename.lower() == 'yes'


def perform_rename(root, file, lowercase, uppercase):
    # save original filename
    original_filename = file

    # set original file path
    original_path = os.path.join(root, file)

    # replace substrings
    for substring, replacement in replacements.items():
        if substring in file:
            file = file.replace(substring, replacement)

            if lowercase:
                file = file.lower()

            if uppercase:
                file = file.upper()

    # set new file path
    new_path = os.path.join(root, file)

    if original_path != new_path:
        global renamed_count
        renamed_count += 1

        # rename file
        os.rename(original_path, new_path)

        output_string = f"'{original_filename}' >>> '{file}'"
        renamed_files.append(output_string)


def rename_files(target_path, lowercase=False, uppercase=False):
    # raise an error if user passed True for lowercase AND uppercase arguments
    if lowercase is True and uppercase is True:
        error_string = "Lowercase OR uppercase argument can be True, but not both."
        raise ValueError(error_string)

    is_confirmed = set_confirmation(target_path)

    if is_confirmed:
        for root, _, files in os.walk(target_path):
            for file in files:
                # append root/new path before renamed file
                path_string = f'\n{root}\n'
                if path_string not in renamed_files:
                    renamed_files.append(path_string)

                perform_rename(root, file, lowercase, uppercase)

        completed_string = f'\nOperation completed: {renamed_count if renamed_count else "No"} total files were renamed.'
        print(completed_string)

        current_time = datetime.now()

        # log results
        with open(f'{current_time}.txt', 'a') as log:
            log.write(f'Rename operation completed at: {current_time}\n')
            log.write(f'\n{renamed_count} total files renamed\n')
            log.write('-----------------------\n')
            log.write('\n'.join(renamed_files))
    else:
        print('\nOperation aborted: Failed to confirm.')


get_counts(target_path)
rename_files(target_path, lowercase, uppercase)
