from utils.objects import ObjectsFactory

__author__ = 'roberto'

import unittest


class ObjectsFactoryTestCase(unittest.TestCase):

    def test_create_base_element(self):

        be = ObjectsFactory.create_base_element()

        be.objectId = 1
        be.objectName = "Base Element"

        print(be.objectId, be.objectName)

        self.assertIsNotNone(be)


if __name__ == '__main__':
    unittest.main()
