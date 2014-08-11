#!/usr/bin/env python2
from utils.objects import BaseFactory

__author__ = 'roberto'

import sys


def fac(n):
    """Factorial. Max recursion: 999"""

    if n == 1 or n == 0: return 1
    return n * fac(n - 1)


def cb(n, k):
    """Binomial coefficient."""

    return fac(n) / (fac(k) * fac(n - k))


def pythatriples():
    """FInd pythagorean triples up to 1000."""

    #triples = []

    with BaseFactory.create_structured_writer_ex("data/pythatriples1000.txt", ',') as sw:

        for a in range(1, 1001):
            print(a)
            for b in range(1, 1001):
                for c in range(1, 1001):
                    #print("{:4}, {:4}, {:4}".format(a, b, c))
                    if a ** 2 + b ** 2 == c ** 2:
                        x = (str(a), str(b), str(c))
                        #triples.append(x)
                        sw.append_structured(x)

    #return triples


if __name__ == '__main__':
    if len(sys.argv) > 2:
        n = float(sys.argv[1])
        k = float(sys.argv[2])
        print(cb(n, k))
    else:
        print("plase specify n, k")


    pythatriples()

    # with BaseFactory.create_structured_writer_ex("data/structuredtest.txt") as sw:
    #     sw.append_structured(('1', '2', '3', '4', '5'), ',')
    #     sw.append_structured(('1', '2', '5'), ',')
    #     sw.append_structured(('1', '3', '4', '5'), ',')
    #     sw.append_structured(('1', '2', '3'), ',')

    # with BaseFactory.create_structured_reader_ex("data/structuredtest.txt", ',') as sr:
    #
    #     for record in sr:
    #         print(record)