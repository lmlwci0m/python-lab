__author__ = 'roberto'


from utils import encutils


def readfile(filename):
    """Read a text file with default package encoding."""

    with open(filename, encoding=encutils.DEFAULT_FILE_ENCODING) as f:
        return f.read()


def read_binary_file(filename):
    """Read a text file with default package encoding."""

    with open(filename, "rb") as f:
        return f.read()