__author__ = 'roberto'

import unittest

from mathutils.juliaset import *


class JuliasetTestCase(unittest.TestCase):

    def test_run_julia_set(self):
        run_julia_set()
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
