__author__ = 'roberto'

import sys


consoleinput = input
if sys.version_info.major == 2:
    consoleinput = raw_input