__author__ = 'Roberto'

import os

win_volume = "c:\\"

def traverse(dir_path):


    try:
        entries = os.listdir(dir_path)

    except PermissionError as err:
        print(err)
        return

    for entry in entries:
        entry_full_path = os.path.join(dir_path, entry)

        if os.path.isdir(entry_full_path):
            traverse(entry_full_path)

        elif os.path.isfile(entry_full_path):

            try:
                with open(entry_full_path, "rb") as f:
                    content = f.read(3)

                    if content == bytes([0xFF, 0xD8, 0xFF]):
                        print(entry_full_path)
            except PermissionError as err:
                print(err)

traverse(win_volume)