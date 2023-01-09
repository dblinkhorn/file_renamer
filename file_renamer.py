# !/usr/bin/python

import os
import sys
import json
from datetime import datetime
import argparse


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


is_script = __name__ == '__main__'


# only run parser logic if file is run as a script
if is_script:
    # define the parser
    parser = argparse.ArgumentParser(description='Parse arguments from CLI.')

    # define arguments
    parser.add_argument('--target-path', action="store",
                        dest='target_path', default="null")
    parser.add_argument('--string', action="store",
                        dest='string', default="null")
    parser.add_argument('--replacement', action="store",
                        dest='replacement', default="null")
    parser.add_argument('--lowercase', action="store",
                        dest='lowercase', default=False)
    parser.add_argument('--uppercase', action="store",
                        dest='uppercase', default=False)

    args = parser.parse_args()

    # set arguments
    target_path = args.target_path
    string = args.string
    replacement = args.replacement
    lowercase = args.lowercase
    uppercase = args.uppercase

    replacements = {
        string: replacement
    }

    if target_path == "null" or string == "null" or replacement == "null":
        print(("Please specify an argument for "
               "--target-path, --string, and --replacement."))
        sys.exit()

    if not os.path.exists(target_path):
        print("Path does not exist.")
        sys.exit()

    # get counts of inspected file and directories
    file_count, dir_count = get_counts(target_path)

# set when run as a module
else:
    target_path = ''

    # substring/regex replacement rules will be built here in UI
    replacements = {}

    lowercase = False
    uppercase = False


def set_confirmation(target_path, file_count, dir_count):
    '''Used when run as a script to display to user the number of files and
    directories that will be inspected. Returns True if user confirms.'''

    print(f'\nSelected target directory: {target_path}')

    subdirs_string = f', including {dir_count} sub-directories,'
    count_string = (f'\n{file_count} files'
                    f'{subdirs_string if dir_count else ""} '
                    'will be inspected.\n')

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
    '''Performs the rename logic as well as setting up the JSON log data.
    Takes the target path, optional lowercase or uppercase forcing arguments.
    'base_log' is used to pass the base JSON log data to the recursive calls.'''
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

    # traverse files and directories
    with os.scandir(path) as iterator:
        for item in iterator:
            # exclude hidden files and directories
            if not item.name.startswith('.'):
                # add any sub-directories to 'children' of current directory
                if item.is_dir():
                    children.append(
                        perform_rename(item.path, replacements, lowercase,
                                       uppercase, base_log))
                # if 'item' is a file
                else:
                    base_log['files_inspected'] += 1
                    for substring, replacement in replacements.items():
                        if substring in item.name:
                            new_name = item.name.replace(
                                substring, replacement)
                            if lowercase:
                                new_name = new_name.lower()
                            if uppercase:
                                new_name = new_name.upper()
                            new_path = os.path.join(path, new_name)
                            os.rename(item.path, new_path)
                            base_log['files_renamed'] += 1
                            files.append({
                                'original_name': item.name,
                                'new_name': new_name,
                            })
                            break
            else:
                # if 'item' is a hidden directory, continue
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
    '''Accepts a path argument. Performs rename operation and displays summary
    information to the user.'''
    def rename():
        # result will be JSON log object
        result = perform_rename(target_path, replacements,
                                lowercase, uppercase)

        timestamp = result['timestamp']

        # create log file
        with open(f'renamer_log--{timestamp}.json', 'a') as log:
            log.write(json.dumps(result, indent=4, default=str))

        files_renamed = (result['files_renamed']
                         if result['files_renamed'] > 0 else "No")
        result_msg = (f'\nOperation completed: '
                      f'{files_renamed} files were renamed.')

        return result_msg

    if is_script:
        is_confirmed = set_confirmation(target_path, file_count, dir_count)
        if is_confirmed:
            result_msg = rename()
            print(result_msg)
        else:
            print('\nOperation aborted: Failed to confirm.')
    else:
        return rename()


if is_script:
    run_renamer(target_path)
