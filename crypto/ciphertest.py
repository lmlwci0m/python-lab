__author__ = 'rpancald'

import unittest
import crypto.cipherbasic


class MyTestCase(unittest.TestCase):
    def test_something(self):
        blocks = bytearray([1, 2, 3, 4, 5, 6])
        cipher = crypto.cipherbasic.Transposition(blocks)
        cipher.encode()
        print(cipher)


if __name__ == '__main__':
    unittest.main()
