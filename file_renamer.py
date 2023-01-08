# !/usr/bin/python

import os
import sys
import json
from datetime import datetime
import argparse

# Define the parser
parser = argparse.ArgumentParser(description='parse arguments from cli')

parser.add_argument('--target-path', action="store", dest='target_path', default="null")
parser.add_argument('--name', action="store", dest='name', default="null")
parser.add_argument('--replacement', action="store", dest='replacement', default="null")
args = parser.parse_args()
target_path = args.target_path
name = args.name
replacement = args.replacement

replacements = {
    name:replacement
}

if target_path == "null" or name == "null" or replacement == "null":
    print("Please specify an argument for --target-path --name and --replacement")
    exit(1)

if os.path.exists(target_path) == False:
    print("Path does not exist")
    exit(1)

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


lowercase = False
uppercase = False


def run_renamer(target_path):
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
run_renamer(target_path)
