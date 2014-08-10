__author__ = 'roberto'


def print_iter(name, obj):

    print(name)

    obj_it = iter(obj)
    while True:
        try:
            x = obj_it.__next__()
            print(x, end=' ')
        except StopIteration:
            break
    print()


def print_for(name, obj):

    print(name)

    for x in obj:
        print(x, end=' ')
    else:
        print()