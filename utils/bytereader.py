#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# bytereader.py: simple program for read bytes of a file.

__author__ = 'roberto'

from utils import objects
import sys

MESSAGE_USAGE = """No input file specified.
Usage:
        bytereader.py inputfile [outputfile]
"""

MESSAGE_USAGE_2 = """Offset and length must be specified as integers.
Usage:
        bytereader.py inputfile [outputfile | offset, size]
"""


def main():

    if len(sys.argv) < 2:
        print(MESSAGE_USAGE)
        sys.exit(0)

    output = None if (len(sys.argv) != 3) else sys.argv[2]

    byte_reader = objects.BaseFactory.create_byte_reader(sys.argv[1], 32)  # No operations

    byte_reader.do_read()  # Read entire file

    if not output:

        if len(sys.argv) == 4:
            try:
                offset = int(sys.argv[2])
                size = int(sys.argv[3])
            except ValueError:
                print(MESSAGE_USAGE_2)
                sys.exit(0)
            byte_reader.do_print_block(offset, size)

        else:
            byte_reader.do_print()

    else:
        with open(output, "w") as f:
            byte_reader.do_print(f)



if __name__ == '__main__':
    main()