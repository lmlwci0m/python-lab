__author__ = 'roberto'

import unittest
from extensions import blocks


class TestExtensions(unittest.TestCase):
    def test_blocks(self):
        print(blocks)
        print(blocks.get_blocks())


if __name__ == '__main__':
    unittest.main()
