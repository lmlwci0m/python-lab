__author__ = 'roberto'

import uuid
import sys

num = int(sys.argv[1])

replace = True

for x in range(num):
    if replace:
        print(str(uuid.uuid4()).replace('-', ''))
    else:
        print(uuid.uuid4())