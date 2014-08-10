__author__ = 'roberto'

import os

win_volume = "c:\\"

MAGIC_NUMBER = [0xFF, 0xD8, 0xFF]

def traverse(dir_path, magic=MAGIC_NUMBER):
    """Scan a directory and its subdirectories for files respecting a specified magic number."""

    try:
        entries = os.listdir(dir_path)

    except PermissionError as err:
        print(err)
        return

    for entry in entries:
        entry_full_path = os.path.join(dir_path, entry)

        if os.path.isdir(entry_full_path):
            traverse(entry_full_path, magic)

        elif os.path.isfile(entry_full_path):

            try:
                with open(entry_full_path, "rb") as f:

                    content = f.read(len(magic)) # content = f.read(3)

                    if content == bytes(MAGIC_NUMBER):
                        print(entry_full_path)
            except PermissionError as err:
                print(err)

traverse(win_volume)