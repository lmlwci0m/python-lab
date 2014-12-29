__author__ = 'roberto'

import sys


DEFAULT_FILE_ENCODING = "utf-8"


def getsystemenc():
    """From Python 3.2 cannot be None"""

    return sys.getfilesystemencoding()