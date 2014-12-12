import unittest
from mathutils import basic

__author__ = 'roberto'


class TestMath(unittest.TestCase):
    def test_sum(self):

        index_base = basic.get_expicit_range(1, 10000)

        for x in index_base:
            print(x)

        set1 = {1, 2, 3, 4, 5, 6}
        set2 = {2, 8, 9}

        print(basic.do_union(set1, set2))


if __name__ == '__main__':
    unittest.main()