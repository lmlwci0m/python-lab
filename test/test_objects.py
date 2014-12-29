__author__ = 'roberto'

from utils.objects import ObjectsFactory

import unittest


#
# def func(arg1[=defval], ... , argN[=defval], *args, [argN1[=defval , ... , argNN[=defval], **kwargs])
#

def execute_new(first_arg, second_arg="aaaaaa", *args):  # , **kwargs
    """Module level function.
    ok: execute("aa", secondArgument="uuuhhhhh", uh="first",  ah="second")
    ko: execute("aa", "first", "second", secondArgument="uuuhhhhh")
    """

    print(first_arg)
    print(second_arg)
    if args:
        print(args[0])


def execute(first_arg, *args, second_arg="aaaaaa"):  # , **kwargs
    """Module level function.
    ok: execute("aa", "first", "second", secondArgument="uuuhhhhh")
    ko: execute("aa", "first", secondArgument="uuuhhhhh", "second")
    """

    print(first_arg)
    print(second_arg)
    if args:
        print(args[0])


class ObjectsFactoryTestCase(unittest.TestCase):

    def test_manage_base_element(self):

        be = ObjectsFactory.create_base_element()

    def test_create_base_element(self):

        be = ObjectsFactory.create_base_element()

        be.objectId = 1
        be.objectName = "Base Element"

        print(be.objectId, be.objectName)

        self.assertIsNotNone(be)

        execute("aa", "first", "second", second_arg="uuuhhhhh")
        execute_new("aa", second_arg="uuuhhhhh")  # , uh="first",  ah="second"

        i = 0
        try:

            def ohloop():
                nonlocal i
                i += 1
                ohloop()

            ohloop()

        except RuntimeError:
            print(i)

if __name__ == '__main__':
    unittest.main()
