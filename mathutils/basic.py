#!/usr/bin/env python2

__author__ = 'roberto'

import sys

def fac(n):
    """Max recursion: 999"""

    if n == 1 or n == 0: return 1
    return n * fac(n - 1)

def cb(n, k):
    return fac(n) / (fac(k) * fac(n - k))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        n = float(sys.argv[1])
        k = float(sys.argv[2])
        print(cb(n, k))
    else:
        print("plase specify n, k")
