from utils import objects
from utils.printingutils import print_iter, print_for

__author__ = 'roberto'


class TestListIterator(object):
    """Iterator test implementation."""

    def __init__(self, parent):
        self.parent = parent
        self.counter = 0
        self.count = len(parent.elements)

    def __next__(self):
        if self.counter == self.count: # Exhaustion
            raise StopIteration
        ref, self.counter = self.counter, self.counter + 1
        return str(self.parent.elements[ref])

    def __iter__(self):
        return TestListIterator(self.parent)


class TestList(object):

    def __init__(self):
        self.elements = [1,2,3,4]

    def __iter__(self):
        return TestListIterator(self)


def main():
    test_str = 'string'
    test_list = ['element1', 'element2', 'element3']
    test_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

    print_iter("test_str", test_str)

    print_iter("test_list", test_list)

    print_iter("test_dict", test_dict)

    test_elements = TestList()

    print_for("test_elements", test_elements)
    print_iter("test_elements", test_elements)

    br = objects.BaseFactory.create_byte_reader_ex('data/test.txt', 32)
    with open("data/dataout.txt", "w") as f:
        br.do_print(f)


if __name__ == '__main__':
    main()