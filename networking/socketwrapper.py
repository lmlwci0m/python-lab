__author__ = 'roberto'

from contextlib import contextmanager
import socket

#
# file:///Library/Frameworks/Python.framework/Versions/3.4/Resources/English.lproj/Documentation/library/contextlib.html?highlight=contextmanager#contextlib.contextmanager
#

@contextmanager
def socketcontext(*args, **kw):
    s = socket.socket(*args, **kw)
    yield s
    s.close()