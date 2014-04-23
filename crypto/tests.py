from crypto.analysis import FreqAnalysis

__author__ = 'Roberto'

from functools import partial
from utils.objects import BaseFactory, ExtendedFactory
from crypto.cipherbasic import Transposition, SingleByteXor, Vernam

def E(K, M):
    return M


def D(K, C):
    return C


def caesar_enc(text):
    return "".join(chr(ord(x) + 3) for x in text)


def caesar_dec(text):
    return "".join(chr(ord(x) - 3) for x in text)

def sub_enc(key, text):
    return "".join(chr(ord(x) + key) for x in text)


def sub_dec(key, text):
    return "".join(chr(ord(x) - key) for x in text)


def t_enc(key, block):
    return block + key


def t_dec(key, block):
    return block - key


def main():

    #M = ""
    #K = ""

    #enc = partial(E, K)
    #dec = partial(D, K)

    #print(M == dec(enc(M)))

    #br = BaseFactory.create_byte_reader("data/test.txt")
    #br.do_read()
    #br.do_print()

    #lb = br.blocks[-1]
    #print("{:02x}".format(lb))
    #print(lb == 0x0a)

    # br.blocks = bytearray(br.blocks)
    # for index, block in enumerate(br.blocks):
    #     br.blocks[index] = t_enc(KEY, block)
    #
    # writer = BaseFactory.create_writer("data/test2.txt")
    # writer.write_bytes(br.blocks)
    #
    # br2 = BaseFactory.create_byte_reader("data/test2.txt")
    # br2.do_read()
    #
    # br2.blocks = bytearray(br2.blocks)
    # for index, block in enumerate(br2.blocks):
    #     br2.blocks[index] = t_dec(KEY, block)
    #
    # writer3 = BaseFactory.create_writer("data/test3.txt")
    # writer3.write_bytes(br2.blocks)

    PLAIN_TEXT = "data/test.txt"
    CIPHER_TEXT = "data/test2.txt"
    DECIPHER_TEXT = "data/test3.txt"


    KEY = bytes([0x34, 0x76, 0xff, 0xff, 0xaa])

    encoder = Vernam(BaseFactory.create_byte_reader(PLAIN_TEXT).do_read().blocks)

    BaseFactory.create_writer(CIPHER_TEXT).write_bytes(encoder.encode(KEY).encblocks)

    decoder = Vernam(BaseFactory.create_byte_reader(CIPHER_TEXT).do_read().blocks)

    BaseFactory.create_writer(DECIPHER_TEXT).write_bytes(decoder.decode(KEY).encblocks)

    check1 = BaseFactory.create_byte_reader(PLAIN_TEXT)
    check2 = BaseFactory.create_byte_reader("data/test3.txt")

    check1.do_read()
    check2.do_read()

    check1.do_print()
    print()
    check2.do_print()

    print(check1 == check2)

    # match = True
    # if len(check1.blocks) != len(check2.blocks):
    #     match = False
    # if match:
    #     for index, block in enumerate(check1.blocks):
    #         if check2.blocks[index] != block:
    #             match = False
    #             break
    #
    # print(match)

    data = ExtendedFactory.ByteReaderExtended()



    data.do_get(bytes('fsadjifjasoidòfjasvdòiofjasdòo', 'utf-8'))

    data.do_print_block(0, 4)

    fa = FreqAnalysis()

    for key in fa.sylls:
        print("{}: {}".format(key, fa.sylls[key]))


def main2():

    bytes_obj = BaseFactory.create_byte_reader("data/test.txt").do_read()

    t = Transposition(bytes_obj.blocks)

    t.do_blocks()


if __name__ == '__main__':
    main2()
