import hashlib
import os
import sys

__author__ = 'roberto'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""No input file specified.
Usage:
        checksum.py inputfile
""")
        sys.exit(0)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print("Input file {} does not exists".format(filename))
        sys.exit(0)

    with open(filename, "rb") as f:
        content = f.read()

        m = hashlib.sha256()

        m.update(content)

        print(m.hexdigest())