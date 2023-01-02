File Renamer

This script inspects a target directory and will evaluate all files in the directory, and in all
sub-directories, and rename any file whose name matches user-specified rename rules. Before
running this script, you will need to specify the following values within 'file_renamer.py':

1.  target_path -- This is the root folder the script will inspect.

2.  replacements -- The keys of this dictionary will be substrings or regex patterns that you want
    to be replaced in an inspected file's name. The values of the dictionary will the values you
    want to replace the substring or regex pattern (key) with. For example, if you specify this...

        replacements = {
            "aloha": "hello"
        }

    ...then any inspected file containing the substring "aloha" in its name will have that sub-
    string replaced with "hello". If you have a file whose name is "aloha_world.txt" then the new
    file name would be "hello_world.txt".

3.  lowercase -- If this is set to 'True', then an inspected file's new name will be forced to
    lowercase. Only files whose names would also cause them to be renamed by one of the
    'replacements' rules will be affected.

4.  uppercase -- Same as above except as uppercase. If you set 'lowercase' and 'uppercase' to
    'True' it will throw a ValueError.

When the script is run you will be shown the total number of files and directories to be inspected,
and asked to confirm the rename operation. If no files are found, the script will auto-abort.
Hidden files and directores will not be inspected, nor will directory names be affected. Once a
successful rename operation has been performed, a JSON log file will be created in the same
directory that contains the script.
