#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Roberto'

import sys
import os
import stat


def main():
    
    if len(sys.argv) < 2:
        print("Please specify a filename.")
        print("""Usage:
    newscript.py filename [module1 [, module2 [, ...]]]
        
""")
        return
        
    filename = sys.argv[1]
    
    imports = sys.argv[2:] if len(sys.argv) > 2 else None
    
    importsection = "" if not imports else "\n".join(["import {0:s}".format(module) for module in imports])
    
    scriptcontent = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

{0:s}


def main():
    pass


if __name__ == '__main__':
    main()

"""

    with open(filename, "w") as f:
        f.write(scriptcontent.format(importsection))
        
    #mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
    #mode = mode | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
    #mode = mode | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH
    
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
    mode = mode | stat.S_IRGRP | stat.S_IXGRP
    mode = mode | stat.S_IROTH | stat.S_IXOTH
        
    os.chmod(filename, mode)
    

if __name__ == '__main__':
    main()
    sys.exit(0)