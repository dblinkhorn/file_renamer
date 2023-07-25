**File Renamer**

This script inspects a target directory and will evaluate all files in the directory, and in all
sub-directories, and rename any file whose name matches user-specified rename rules. If you are
using this script from the command line, before running the script, you will need to specify the
following values within `file_renamer.py`:

-   `target_path`: This is the root folder the script will inspect.

-   `replacements`: The keys of this dictionary will be substrings or regex patterns that you want
    to be replaced in an inspected file's name. The values of the dictionary will the values you
    want to replace the substring or regex pattern (key) with. For example, if you specify this:

         replacements = {
             "aloha": "hello"
         }

    ...then any inspected file containing the substring `aloha` in its name will have that sub-
    string replaced with `hello`. If you have a file whose name is `aloha_world.txt` then the new
    file name would be `hello_world.txt`.

-   `lowercase`: Can be `True` or `False`. If this is set to 'True', then an inspected file's new
    name will be forced to lowercase. Only files whose names would also cause them to be renamed by
    one of the 'replacements' rules will be affected. (default: `False`)

-   `uppercase`: Same as above except as uppercase. If you set both 'lowercase' and 'uppercase' to
    'True' it will throw a ValueError. (default: `False`)

In addition to specifying the above values within the `file_renamer.py` file itself, you can
also specify these values by using arguments from the command line. This use-case is most
appropriate for simpler, single character or single string replacements. You can specify the following arguments:

-   `--target_path`: The target directory to begin renaming files. (default: `None`)
-   `--string`: Specifies the character(s) in a filename that should be replaced. (default: `None`)
-   `--replacement`: Specifies the value to replace the matched `--string` value. (default: `None`)
-   `--lowercase`: Can be `True` or `False`. Enforces lowercase characters in the rename operation.
    All affected files whose names contain any non-lowercase characters will be replaced with their
    lowercase equivalents. (default `False`)
-   `--uppercase`: Same as above except enforces uppercase.

\*\*\*Setting both `--lowercase` and `--uppercase` will result in a `ValueError`.\*\*\*

When the script is run you will be shown the total number of files and directories to be inspected,
and asked to confirm the rename operation. If no files are found, the script will auto-abort.
Hidden files and directores will not be inspected, nor will directory names be affected. Once a
successful rename operation has been performed, a JSON log file will be created in the same
directory that contains the script.
