from utils.printingutils import print_iter, print_for

__author__ = 'roberto'


class TestList(object):

    def __init__(self):
        self.elements = [1,2,3,4]

    def __next__(self):
        if self.counter == len(self.elements):
            raise StopIteration()
        retval = self.elements[self.counter]
        self.counter += 1
        return str(retval)

    def __iter__(self):
        self.counter = 0
        return self


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

if __name__ == '__main__':
    main()