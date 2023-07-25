## File Renamer

This script inspects a target directory and will evaluate all files in the directory, and in all
sub-directories, and rename any file whose name matches user-specified rename rules.

When running this script you must specify the following arguments:

-   `--target_path`: The target directory to begin renaming files. (default: `None`)
-   `--string`: Specifies the character(s) in a filename that should be replaced. (default: `None`)
-   `--replacement`: Specifies the value to replace the matched `--string` value. (default: `None`)
-   `--lowercase`: Can be `True` or `False`. Enforces lowercase characters in the rename operation.
    All affected files whose names contain any non-lowercase characters will be replaced with their
    lowercase equivalents. (default `False`)
-   `--uppercase`: Same as above except enforces uppercase.

**Setting both `--lowercase` and `--uppercase` to `True` will result in a `ValueError`.**

As an example, if you had a lot of files containing `foo` in the filename, and you wanted to
replace those instances with `bar` you would run the following:

```
python file_renamer.py --target_path my_folder --string foo --replacement bar
```

A file whose name was `foobar.txt` would become `barbar.txt`.

## Renamer UI

You can also run this script using the UI interface. You will first need to install all dependecies
by running:

```
pip install -r requirements.txt
```

Then you can run the UI:

```
python renamer_ui.py
```

When the script is run you will be shown the total number of files and directories to be inspected,
and asked to confirm the rename operation. If no files are found, the script will auto-abort.
Hidden files and directores will not be inspected, nor will directory names be affected. Once a
successful rename operation has been performed, a JSON log file will be created in the same
directory that contains the script.
