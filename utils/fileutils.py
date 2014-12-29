__author__ = 'roberto'

import os
from utils.objects import BaseFactory


from utils import encutils


def readfile(filename):
    """Read a text file with default package encoding."""

    with open(filename, encoding=encutils.DEFAULT_FILE_ENCODING) as f:
        return f.read()


def read_binary_file(filename):
    """Read a binary file with default package encoding."""

    with open(filename, "rb") as f:
        return f.read()


def main():
    pass

if __name__ == '__main__':
    queue = BaseFactory.create_queue()

    queue.enqueue(123)
    queue.enqueue(43543534)
    queue.enqueue(756535463)

    while not queue.is_empty():
        print(queue.dequeue())

    info = os.stat("D:\\jboss-eap-6.2\\standalone")

    for x in dir(info):
        print(x, getattr(info, x))