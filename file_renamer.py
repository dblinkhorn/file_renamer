# !/usr/bin/python

import os
import sys
import json
from datetime import datetime


# [ USER OPTIONS ] ***********************************************************

# specify path to root folder
# target_path = '/home/example-user/example-folder'
target_path = '/home/dblinkhorn/example'

# specify substring/regex replacements
replacements = {
    # target: replacement
    # '%20': '_',
    # ' ': '_',
    'asdf': 'asda'
}

# change either values below to 'True' (but not both) to force desired case
# only affects files whose name includes a defined substring/regex
# in 'replacements'
lowercase = False
uppercase = False

# ****************************************************************************


def get_counts(target_path):
    file_count = 0
    dir_count = 0  # count does not include 'target_path' directory
    for _, dirs, files in os.walk(target_path):
        # remove hidden files and directories
        files = [file for file in files if not file[0] == '.']
        dirs[:] = [dir for dir in dirs if not dir[0] == '.']
        file_count += len(files)
        dir_count += len(dirs)
    return [file_count, dir_count]


file_count, dir_count = get_counts(target_path)


def set_confirmation(target_path, file_count, dir_count):
    print(f'\nSelected target directory: {target_path}')
    subdirs_string = f', including {dir_count} sub-directories,'
    count_string = (f'\n{file_count} files'
                    f'{subdirs_string if dir_count else ""} '
                    'will be affected...\n')
    if file_count:
        print(count_string)
    else:
        print('\nOperation aborted: No files found.')
        sys.exit()
    confirm_string = ('Are you sure you wish to proceed '
                      'with rename operation? (y/n): ')
    confirm_input = input(confirm_string)
    return confirm_input.lower() == 'y' or confirm_input.lower() == 'yes'


def perform_rename(path, replacements, lowercase=False,
                   uppercase=False, base_log=None):
    # raise an error if user passed True for
    # 'lowercase' AND 'uppercase' arguments
    if lowercase is True and uppercase is True:
        error_string = ("'lowercase' OR 'uppercase' argument can be True, "
                        'but not both.')
        raise ValueError(error_string)
    # if 'base_log' argument is not passed, current path is 'target_path'
    # this means it's the first execution of 'perform_rename()'
    is_target_path = base_log is None
    if is_target_path:
        base_log = {
            'timestamp': datetime.now(),
            'directories_inspected': 0,
            'files_inspected': 0,
            'files_renamed': 0,
            'replacement_rules': replacements,
            'target_path': path,
        }
    files = []
    children = []
    with os.scandir(path) as iterator:
        for item in iterator:
            # exclude hidden files and directories
            if not item.name.startswith('.'):
                # add any sub-directories to 'children' of current directory
                if item.is_dir():
                    children.append(
                        perform_rename(item.path, replacements, lowercase,
                                       uppercase, base_log)
                    )
                # if 'item' is a file
                else:
                    base_log['files_inspected'] += 1
                    for substring, replacement in replacements.items():
                        if substring in item.name:
                            new_name = item.name.replace(
                                substring, replacement)
                            new_path = os.path.join(path, new_name)
                            os.rename(item.path, new_path)
                            base_log['files_renamed'] += 1
                            files.append({
                                'original_name': item.name,
                                'new_name': new_name,
                            })
                            break
            else:
                continue
    base_log['directories_inspected'] += 1
    # start building 'directory' object
    directory = {'directory': path}
    # add 'files' and 'children' to 'directory' object
    if files:
        directory.update({'files': files})
    if children:
        directory.update({'children': children})
    if is_target_path:
        rename_data = {'rename_data': [directory]}
        # add 'base_log' keys/values to 'rename_data'
        directory = base_log | rename_data
    return directory


def run_renamer(target_path):
    is_confirmed = set_confirmation(target_path, file_count, dir_count)
    if is_confirmed:
        result = perform_rename(target_path, replacements,
                                lowercase, uppercase)
        timestamp = result['timestamp']
        # create log file
        with open(f'renamer_log--{timestamp}.json', 'a') as log:
            log.write(json.dumps(result, indent=4, default=str))
        files_renamed = (result['files_renamed']
                         if result['files_renamed'] > 0 else "No")
        completed_string = (f'\nOperation completed: '
                            f'{files_renamed} files were renamed.')
        print(completed_string)
    else:
        print('\nOperation aborted: Failed to confirm.')


run_renamer(target_path)
