__author__ = 'roberto'


import types
import unittest


def custom_handler(self, param):
    print("Custom handler: " + param)


class HandlerObject(object):

    def __init__(self, handler=None):
        if handler:
            self.handler = types.MethodType(handler, self)
        else:
            self.handler = self.__default_handler

    def __default_handler(self, param):
        print("Default handler: " + param)

    def do(self, param):
        self.handler(param)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = HandlerObject()
        print(a.handler)
        a.do("test 1")
        a = HandlerObject(custom_handler)
        print(a.handler)
        a.do("test 2")

if __name__ == '__main__':
    unittest.main()
