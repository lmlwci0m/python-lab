#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Roberto'


import sqlite3
import string
import array
import stat
import os


class UtilsFactory(object):

    class Environment(object):
        """Class for environment management."""

        SEP = os.pathsep

        PATH_KEY = 'PATH'

        JAVA_KEYS = [
            'JAVA_HOME',
            'M2_HOME',
            'CLASSPATH',
            'M2',
        ]

        PYTHON_KEYS = [
            'PYTHONSTARTUP',
            'PYTHONUNBUFFERED',
            'PYTHONPATH',
        ]

        GO_KEYS = [
            'GOROOT',
            'GOPATH',
        ]

        WIN_KEYS = [
            'SYSTEMROOT',
            'WINDIR',
            'OS',
        ]

        FORMAT_STR="{}={}"

        def __init__(self):
            self.env = os.environ
            self.path = self.env[self.PATH_KEY].split(self.SEP)

        def _show_env(self, key_list, format_str=FORMAT_STR):
            for entry in key_list:
                print(format_str.format(entry, self.env.get(entry, '[None]')))

        def show_path(self):
            for entry in self.path:
                print(entry)

        def show_java(self):
            self._show_env(self.JAVA_KEYS)

        def show_python(self):
            self._show_env(self.PYTHON_KEYS)

        def show_all(self):
            for key in self.env.keys():
                print(self.FORMAT_STR.format(key, self.env[key]))



    class FileMasks(object):
        """Wrapper for chmod operations. Includes various methods for add and removal of permissions to filenames.
    Usage:
        fmm = UtilsFactory.create_filemasks()
        fmm.remove_everything_but_owner("file.txt")

        """

        def __init__(self):

            # rwx --- ---
            self.owner = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR

            # --- rwx ---
            self.group = stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP

            # --- --- rwx
            self.other = stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH

            # r-- r-- r--
            self.p_read = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH

            # -w- -w- -w-
            self.p_write = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH

            # --x --x --x
            self.p_exec = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

        @staticmethod
        def add(filename, modeadd):
            mode = os.stat(filename).st_mode
            mode = mode | modeadd
            os.chmod(filename, mode)

        @staticmethod
        def remove(filename, moderem):

            mode = os.stat(filename).st_mode
            mode = mode & ~moderem
            os.chmod(filename, mode)

        def add_everything(self, filename):
            """Add all permissions for everyone ('rwx rwx rwx' +rwx) to filename."""

            self.add(filename, self.owner | self.group | self.other)

        def remove_everything_but_owner(self, filename):
            """Remove all permissions for everyone but tje owner ('--- rwx rwx') from filename."""

            self.remove(filename, self.group | self.other)

        def add_everyone_read(self, filename):
            """Add read permissions for everyone ('r-- r-- r--' +r) to filename."""

            self.add(filename, self.p_read)

        def add_everyone_write(self, filename):
            """Add write permissions for everyone ('-w- -w- -w-' +w) to filename."""

            self.add(filename, self.p_write)

        def add_everyone_execute(self, filename):
            """Add execute permissions for everyone ('--x --x --x' +x) to filename."""

            self.add(filename, self.p_exec)

        def remove_everyone_execute(self, filename):
            """Remove execute permissions for everyone ('--x --x --x' -x) from filename."""

            self.remove(filename, self.p_exec)

        def add_group_read(self, filename):
            """Add read permission for group ('--- r-- ---') to filename."""

            self.add(filename, stat.S_IRGRP)

        def add_other_read(self, filename):
            """Add read permission for other ('--- --- r--') to filename."""

            self.add(filename, stat.S_IROTH)

        def remove_group_read(self, filename):
            """Remove read permission for group ('--- r-- ---') to filename."""

            self.remove(filename, stat.S_IRGRP)

        def remove_other_read(self, filename):
            """Remove read permission for other ('--- --- r--') from filename."""

            self.remove(filename, stat.S_IROTH)

        def add_group_write(self, filename):
            """Add write permission for group ('--- -w- ---') to filename."""

            self.add(filename, stat.S_IWGRP)

        def add_other_write(self, filename):
            """Add write permission for other ('--- --- -w-') to filename."""

            self.add(filename, stat.S_IWOTH)

        def remove_group_write(self, filename):
            """Remove write permission for group ('--- -w- ---') from filename."""

            self.remove(filename, stat.S_IWGRP)

        def remove_other_write(self, filename):
            """Remove write permission for other ('--- --- -w-') from filename."""

            self.remove(filename, stat.S_IWOTH)

        def add_owner_execute(self, filename):
            """Add execute permission for owner ('--x --- ---') to filename"""

            self.add(filename, stat.S_IXUSR)

        def add_group_execute(self, filename):
            """Add execute permission for group ('--- --x ---') to filename"""

            self.add(filename, stat.S_IXGRP)

        def add_other_execute(self, filename):
            """Add execute permission for other ('--- --- --x') to filename"""

            self.add(filename, stat.S_IXOTH)

        def remove_owner_execute(self, filename):
            """Remove execute permission for owner ('--x --- ---') from filename"""

            self.remove(filename, stat.S_IXUSR)

        def remove_group_execute(self, filename):
            """Remove execute permission for group ('--- --x ---') from filename"""

            self.remove(filename, stat.S_IXGRP)

        def remove_other_execute(self, filename):
            """Remove execute permission for other ('--- --- --x') from filename"""

            self.remove(filename, stat.S_IXOTH)

    class Flags(object):
        """Management of bit flags in a single byte.
    Usage:
        value = 0b00100111  -> 00100111
        flagger = UtilsFactory.create_flags(value)
        flagger.off(0)      -> 00100110
        flagger.on(4)       -> 00110110
        flagger.on(3)       -> 00111110
        flagger.on(7)       -> 10111110
        flagger.on(6)       -> 11111110
        flagger.off(1)      -> 11111100
        flagger.off(2)      -> 11111000
        """

        def __init__(self, startvalues=0):
            self.values = startvalues
            self.flagson = (
                0b00000001,
                0b00000010,
                0b00000100,
                0b00001000,
                0b00010000,
                0b00100000,
                0b01000000,
                0b10000000,
            )
            self.flagsoff = (
                0b11111110,
                0b11111101,
                0b11111011,
                0b11110111,
                0b11101111,
                0b11011111,
                0b10111111,
                0b01111111,
            )

        def on(self, index):
            """Put value 1 to single bit indexed from the least signigicant (0) to the most significant (7)."""

            try:
                self.values |= self.flagson[index]
            except IndexError as err:
                print(err)

        def off(self, index):
            """Put value 0 to single bit indexed from the least signigicant (0) to the most significant (7)."""

            try:
                self.values &= self.flagsoff[index]
            except IndexError as err:
                print(err)

        def allon(self):
            self.values |= 0xFF

        def alloff(self):
            self.values &= 0x00

        def to_byte(self):
            return self.values.to_bytes(1, 'big')

        def to_bin(self):
            return bin(int.from_bytes(self.to_byte(), 'big'))

    @classmethod
    def create_flags(cls, startvalues):
        return cls.Flags(startvalues)

    @classmethod
    def create_filemasks(cls):
        return cls.FileMasks()

    @classmethod
    def create_environment(cls):
        return cls.Environment()


class TextFactory(object):
    """Text representations."""

    MAX = 256

    @classmethod
    def print_unicode_map(cls):

        for x in range(0, TextFactory.MAX):
            if len(bytes(chr(x), 'utf-8')) <= 2: print(x, chr(x))
            else: return

    @classmethod
    def print_boolean_tables(cls, filename):

        truth_values = [True, False]

        tt_and = [(value1, value2, value1 and value2) for value2 in truth_values for value1 in truth_values]
        tt_or = [(value1, value2, value1 or value2) for value2 in truth_values for value1 in truth_values]

        with open(filename, "w") as f:
            f.write("<html>")
            f.write("<style>")
            f.write("table {")
            f.write("border: 1px solid black;")
            f.write("border-spacing: 0px;")
            f.write("border-collapse: collapse;")
            f.write("}")
            f.write("td {")
            f.write("padding: 10px;")
            f.write("padding-top: 2px;")
            f.write("padding-bottom: 2px;")
            f.write("border: 1px solid black;")
            f.write("font-family: Courier;")
            f.write("}")
            f.write("td.num {")
            f.write("font-weight: bold;")
            f.write("background-color: gray;")
            f.write("color: white;")
            f.write("}")
            f.write("</style>")
            f.write("<body>")
            f.write("<table>")

            f.write("<tr><th>a</th><th>b</th><th>and</th></tr>")

            for a, b, c in tt_and:
                f.write("<tr><td>{0:b}</td><td>{1:b}</td><td class=\"num\">{2:b}</td></tr>".format(a, b, c))

            f.write("</table>")

            f.write("<table>")

            f.write("<tr><th>a</th><th>b</th><th>or</th></tr>")

            for a, b, c in tt_or:
                f.write("<tr><td>{0:b}</td><td>{1:b}</td><td class=\"num\">{2:b}</td></tr>".format(a, b, c))

            f.write("</table>")

            f.write("</body>")
            f.write("</html>")

    @classmethod
    def print_bytes_binary_map(cls, filename=None):
        if not filename:
            for index in range(256):
                print("{0:3d} {0:08b} 0x{0:02x}".format(index))
        else:
            with open(filename, "w") as f:
                f.write("<html>")
                f.write("<style>")
                f.write("table {")
                f.write("border: 1px solid black;")
                f.write("border-spacing: 0px;")
                f.write("border-collapse: collapse;")
                f.write("}")
                f.write("td {")
                f.write("padding: 10px;")
                f.write("padding-top: 2px;")
                f.write("padding-bottom: 2px;")
                f.write("border: 1px solid black;")
                f.write("font-family: Courier;")
                f.write("}")
                f.write("td.num {")
                f.write("font-weight: bold;")
                f.write("background-color: gray;")
                f.write("color: white;")
                f.write("}")
                f.write("</style>")
                f.write("<body>")
                f.write("<table>")
                for index in range(32):
                    f.write("<tr><td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td>".format(index))
                    f.write("<td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td>".format(index+32))
                    f.write("<td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td>".format(index+64))
                    f.write("<td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td>".format(index+128))
                    f.write("<td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td>".format(index+192))
                    f.write("<td class=\"num\">{0:3d}</td><td>{0:08b}</td><td>0x{0:02x}</td></tr>".format(index+224))
                f.write("</table>")
                f.write("</body>")
                f.write("</html>")


class BaseFactory(object):

    class BytesConstraintError(ValueError):
        """Custom Exception."""

        pass

    class BytesUtils(object):
        """Conversion from int to byte and viceversa. Defaults to big endian."""

        default_byte_order = 'big'

        def to_little(self):
            """Set default conversion endianness to little endian."""

            self.default_byte_order = 'little'

        def to_big(self):
            """Set default conversion endianness to big endian."""

            self.default_byte_order = 'big'

        @staticmethod
        def int2byte(intobj):
            """Integer 0 <= x <= 255 -> byte repr."""

            if not 0 <= intobj <= 255:
                raise BaseFactory.BytesConstraintError("intobj must be between 0 and 255")
            return bytes([intobj])

        def byte2int(self, byteobj):
            """Single byte repr -> int object."""

            if len(byteobj) != 1:
                raise BaseFactory.BytesConstraintError("byteobj must be of length 1 (single byte)")
            return int.from_bytes(byteobj, self.default_byte_order) # ok for single byte

        def bytes2int(self, bytesobj, byteorder=default_byte_order):
            """Array of bytes -> int object."""

            return int.from_bytes(bytesobj, byteorder)

    class ConsoleReader(object):
        """Helper utils for reading from console."""

        @staticmethod
        def get(msg="> "):
            """Gets a generic input."""

            return input(msg)

        @staticmethod
        def get_int(msg="> "):
            """Gets a integer input, validating it."""

            while True:
                try:
                    input_value = int(input(msg))
                    return input_value
                except ValueError as err:
                    print(err)

        @staticmethod
        def get_single(msg="> "):
            """Gets a single character input, validating it."""

            while True:
                s = input(msg)
                if len(s) == 1:
                    return s
                else:
                    print("Not a single token.")

    class DB(object):
        """SQLite3 wrapper. """

        def __init__(self, path):
            self.path = path
            self.conn = None

        def connect(self):
            self.conn = sqlite3.connect(self.path)

        def disconnect(self):
            self.conn.close()

        def execute_and_commit(self, query):
            c = self.conn.cursor()
            try:
                c.execute(query)
                self.conn.commit()
            finally:
                c.close()

    class Text(object):
        """Text object (a string)."""

        def __init__(self, text=""):
            self.text = text

        def set_text(self, text):
            self.text = text

        def __str__(self):
            return self.text

    class Writer(object):
        """File object writing helper functions."""

        def __init__(self, filename):
            self.filename = filename

        def write(self, text):
            with open(self.filename, "w") as f:
                return f.write(text)

        def append(self, text):
            with open(self.filename, "a") as f:
                return f.write(text)

        def write_bytes(self, bytes_obj):
            with open(self.filename, "wb") as f:
                return f.write(bytes_obj)

        def append_bytes(self, bytes_obj):
            with open(self.filename, "ab") as f:
                return f.write(bytes_obj)

    class Reader(object):
        """File object reading helper functions."""

        def __init__(self, filename):
            """Only sets filename. No other operation."""

            self.filename = filename

        def read(self):
            """Read entire file as text."""

            with open(self.filename) as f:
                return f.read()

        def read_bytes(self):
            """Read entire file as binary (bytes)."""

            with open(self.filename, "rb") as f:
                return f.read()

    class StructuredWriter(Writer):
        """Newline-separated record writer to file."""

        def append_structured(self, seq, sep):
            with open(self.filename, "a") as f:
                return f.write(sep.join(seq) + "\n")

    class StructuredReader(Reader):
        """Newline-separated record reader from file."""

        def read_structured(self, sep):
            with open(self.filename) as f:
                return [line[0:-1].split(sep) for line in f.readlines()]

    class Queue(object):
        """Array-based integer representation of a queue."""

        max = 1024

        def __init__(self):
            self.elements = array.array("i", range(1024))

            self.index = 0
            self.top = 0

        def enqueue(self, element):
            if self.index == self.max:
                return False
            try:
                self.elements[(self.top + self.index) % self.max] = element
                self.index += 1
            except OverflowError as err:
                print(err)
                return False

            return True
            #self.elements.append(element)

        def dequeue(self):
            if self.index == 0:
                return None

            self.top += 1
            self.index -= 1

            return self.elements[(self.top - 1) % self.max]

            #return self.elements.pop(0)

    class Stack(object):
        """Array-based integer representation of a stack."""

        def __init__(self):
            self.elements = array.array("i")

        def push(self, element):
            self.elements.append(element)

        def pop(self):
            return self.elements.pop()

    class ByteReader(object):
        """A ByteReader is a class that implements functionalities for reading and comparing bytes from files.

        For getting bytes from a file in memory:
        - reader = ByteReader("file.ext")
        - reader.do_read()

        For printing bytes of a file in hexadeciaml format:
        - reader = ByteReader("file.ext") || reader = BaseFactory.create_byte_reader("file.ext")
        - reader.do_read()
        - reader.do_print()       || reader.do_print("output.txt")       ||
          reader.do_print_block() || reader.do_print_block("output.txt")

        For comparing two blocks of bytes (from two files):
        - reader_file_a = BaseFactory.create_byte_reader("file_a")
        - reader_file_b = BaseFactory.create_byte_reader("file_b")
        - reader_file_a.do_read()
        - reader_file_b.do_read()
        - equals = reader_file_a == reader_file_b
        """

        BYTE_FORMAT_ELEMENT = ["{:02x}"]

        def __init__(self, filename, linelen=8):
            self.filename = filename
            self.linelen = linelen
            self.reader = BaseFactory.create_reader(filename)  # Only create reader
            self.formatstr = " ".join(self.BYTE_FORMAT_ELEMENT * self.linelen)
            self.blocks = bytes([])

        def do_read(self):
            self.blocks = self.reader.read_bytes()
            return self

        def do_print_block(self, offset, size, file=None):
            last_format = " ".join(self.BYTE_FORMAT_ELEMENT * size)
            subblock = self.blocks[offset:offset+size]
            outputstr = last_format.format(*subblock)
            self.__do_print(outputstr, file)

        @staticmethod
        def __do_print(strobj, fileobj):
            if fileobj is None:
                print(strobj)
            else:
                print(strobj, file=fileobj)

        def __eq__(self, other):
            """Overload of equality operator. Checks if two byte blocks are equal."""

            match = True
            if len(self.blocks) != len(other.blocks):
                match = False
            if match:
                for index, block in enumerate(self.blocks):
                    if other.blocks[index] != block:
                        match = False
                        break
            return match

        def do_print(self, file=None):

            for bindex in range(0, len(self.blocks), self.linelen):

                # for every block of linelen bytes

                if bindex + self.linelen <= len(self.blocks):

                    subblock = self.blocks[bindex:bindex+self.linelen]  # == linelen block

                    outputstr = self.formatstr.format(*subblock)

                else:

                    subblock = self.blocks[bindex:]  # < linelen block

                    last_linelen = len(self.blocks) - bindex
                    last_format = " ".join(self.BYTE_FORMAT_ELEMENT * last_linelen)

                    outputstr = last_format.format(*subblock)

                self.__do_print(outputstr, file)

    @classmethod
    def create_byte_reader(cls, filename, linelen=8):
        return cls.ByteReader(filename, linelen)

    @classmethod
    def create_stack(cls):
        return cls.Stack()

    @classmethod
    def create_queue(cls):
        return cls.Queue()

    @classmethod
    def create_text(cls):
        return cls.Text()

    @classmethod
    def create_writer(cls, filename):
        return cls.Writer(filename)

    @classmethod
    def create_reader(cls, filename):
        return cls.Reader(filename)

    @classmethod
    def create_structured_writer(cls, filename):
        return cls.StructuredWriter(filename)

    @classmethod
    def create_structured_reader(cls, filename):
        return cls.StructuredReader(filename)

    @classmethod
    def create_db(cls, filename):
        return cls.DB(filename)

    @classmethod
    def create_console_reader(cls):
        return cls.ConsoleReader()

    @classmethod
    def create_bytes_utils(cls):
        return cls.BytesUtils()


class ExtendedFactory(BaseFactory):

    class Text(BaseFactory.Text):

        def __init__(self, text=""):
            self.text = "'{0:s}'".format(text)

        def set_text(self, text):
            self.text = "'{0:s}'".format(text)

    class ByteReaderExtended(BaseFactory.ByteReader):

        #BYTE_FORMAT_ELEMENT = ["{:02x}"]

        def __init__(self, filename=None, linelen=8):
            self.filename = filename
            self.linelen = linelen
            self.formatstr = " ".join(self.BYTE_FORMAT_ELEMENT * self.linelen)

        def do_read(self):
            if self.filename:
                self.reader = BaseFactory.create_reader(self.filename)
                self.blocks = self.reader.read_bytes()
            return self

        def do_get(self, blocks):
            self.blocks = blocks


if __name__ == '__main__':
    # Tests
    bu = BaseFactory.create_bytes_utils()
    for i in range(256):
        assert i == bu.byte2int(bu.int2byte(i))

    q = BaseFactory.create_queue()
    for x in range(1024):
        q.enqueue(x)
    while True:
        x = q.dequeue()
        if x is not None:
            print(x)
        else:
            break

    for x in [543, 765, 4234, 65463, 1235, 6435, 62, 34, 5234, 5, 2456, 13, 62, 456, 234, 51, 346, 2, 346,
              2345, 134, 6, 314, 6, 345, 234, 5]:
        q.enqueue(x)
    while True:
        x = q.dequeue()
        if x is not None:
            print(x)
        else:
            break

    for x in [5435, 534252, 436, 345, 43, 523, 451, 345, 34, 52, 345, 324, 52, 345]:
        q.enqueue(x)
    while True:
        x = q.dequeue()
        if x is not None:
            print(x)
        else:
            break
