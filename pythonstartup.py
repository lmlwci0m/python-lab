__author__ = 'roberto'

#
# Set this file full path to the environment variable PYTHONSTARTUP
#

# Interactive python startup file
print("importing sys")
import sys
print("importing os")
import os

# Print environment variable value
startup = os.environ.get('PYTHONSTARTUP')
print("User environment PYTHONSTARTUP = {0:s}".format(startup))

# Adding toappend paths to sys.path for imports
# C:\Users\rp\PycharmProjects\python-lab
toappend = [
    os.path.dirname(startup),
]
for x in toappend:
    sys.path.append(x)
    print("{0:s} appended to sys path".format(x))
