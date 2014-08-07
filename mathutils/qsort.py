#!/usr/bin/env/python

"""Quicksort in python.

Basic in-place implementation of quicksort algorithm based on 2 way partition.
"""


def iorj(arr, index, i, j):
    """Useful function for printing index position over the array list."""
    
    if index == j and index == i: return " ij"
    if index == j: return "  j"
    elif index == i: return "  i"
    else: return "   "


def part(arr, p, r, debug=True):
    """2-way partitioning algorithm."""
    
    x = arr[p]

    i = p
    j = r
    done = False
    
    while not done:
        
        while True:
            if arr[j] <= x: break
            j = j - 1
            
        while True:
            if arr[i] >= x: break
            i = i + 1
            
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
            j = j - 1
            i = i + 1

            if debug:
                print(", ".join(["{:3}".format(k) for index, k in enumerate(arr)]))
                print("  ".join([iorj(arr, index, i, j) for index, k in enumerate(arr)]))
            
        else:
            
            done = True

            if debug:
                print(", ".join(["{:3}".format(k) for index, k in enumerate(arr)]))
                print("  ".join([iorj(arr, index, i, j) for index, k in enumerate(arr)]))

            arr[p], arr[j] = arr[j], arr[p]

            if debug:
                print(", ".join(["{:3}".format(k) for index, k in enumerate(arr)]))
                print("  ".join([iorj(arr, index, i, j) for index, k in enumerate(arr)]))
                print("-" * 3 * 2 * len(arr))
            
    return j

    
def qs(arr, p, r):
    q = part(arr, p, r)
    if p < r:
        qs(arr, p, q)
        qs(arr, q + 1, r)
        

def quicksort(arr):
    return qs(arr, 0, len(arr)-1)


try:
    arr = [435,1,4,6,56,53,2,7,257,34,72,54,7,348,2,457,34,57,456,4,62,64,26,46,34,62]
    quicksort(arr)
    print(arr)
except RuntimeError as e:
    print(e)
