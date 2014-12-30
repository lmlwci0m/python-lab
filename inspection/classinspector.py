__author__ = 'roberto'

import inspect
from networking.networkcommon import AbstractProtocol


#
# http://stackoverflow.com/questions/3517892/python-list-function-argument-names
#

def get_attrs(cls):
    return {x: getattr(cls, x) for x in dir(cls)}

def type_name(attr):
    return type(attr).__name__


method_flag = ['instancemethod', 'function']

for meth, attr in [(x, getattr(AbstractProtocol, x)) for x in dir(AbstractProtocol) if type(getattr(AbstractProtocol, x)).__name__ in method_flag]:
    print(meth, type(attr).__name__)
    print(inspect.getargspec(attr).args)

for meth, attr in [(x, getattr(AbstractProtocol, x)) for x in dir(AbstractProtocol) if type(getattr(AbstractProtocol, x)).__name__ not in method_flag]:
    print(meth, type(attr).__name__)
print("\n\n\n\n")

for key, value in get_attrs(AbstractProtocol).items():
    print(key, type_name(value))