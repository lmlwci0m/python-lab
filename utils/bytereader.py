#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Roberto'

from utils import objects
import sys


def main():

    if len(sys.argv) < 2:
        print("""No input file specified.
Usage:
        bytereader.py inputfile [outputfile]
""")
        sys.exit(0)

    output = None if (len(sys.argv) != 3) else sys.argv[2]

    br = objects.BaseFactory.create_byte_reader(sys.argv[1], 32)

    br.do_read()

    if not output:
        if len(sys.argv) == 4:
            try:
                offset = int(sys.argv[2])
                size = int(sys.argv[3])
            except ValueError:
                print("""Offset and length must be specified as integers.
Usage:
        bytereader.py inputfile [outputfile | offset, size]
""")
                sys.exit(0)
            br.do_print_block(offset, size)
        else:
            br.do_print()
    else:
        with open(output, "w") as f:
            br.do_print(f)



if __name__ == '__main__':
    main()