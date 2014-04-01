__author__ = 'Roberto'


class Transposition(object):
    """Parametrized version of caesar cipher.

    Key = 3 - Caesar Cipher
    Key = 13 - Russian Army Cipher during WW

    Cost: O(n)
    """

    def __init__(self, blocks):
        self.blocks = blocks
        self.encblocks = bytearray(self.blocks)

    def __enc(self, key, block):
        return (block + key) % 256

    def __dec(self, key, block):
        return (block - key) % 256

    def encode(self, key):
        for index, block in enumerate(self.encblocks):
            self.encblocks[index] = self.__enc(key, block)
        return self

    def decode(self, key):
        for index, block in enumerate(self.encblocks):
            self.encblocks[index] = self.__dec(key, block)
        return self


class SingleByteXor(Transposition):
    """Basic byte to byte xor encryption."""

    def __enc(self, key, block):
        return block ^ key

    def __dec(self, key, block):
        return block ^ key


class Vernam(Transposition):
    """XOR each block with the key reiterated.

    f: {0,1} x {0,1} -> {0,1}
    f(0, 0) = f(1, 1) = 0 # Equal -> false
    f(0, 1) = f(1, 0) = 1 # Not equal -> true

    f(x, y) = f(y, x) # COMMUTATIVITY
    f(x, x) = 0
    f(x, 0) = x # NEUTRALITY (0)
    f(x, f(y, z)) = f(f(x, y), z)

    0 ^ 0 = 1 ^ 1 = 0
    0 ^ 1 = 1 ^ 0 = 1
    x ^ y = y ^ x
    x ^ x = 0
    x ^ 0 = x
    (x ^ (y ^ z)) = ((x ^ y)  ^ z)

    X = (x1, ... , xn)
    Y = (y1, ... , yn)

    X ^ Y = (x1, ... , xn) ^ (y1, ... , yn) =
          = (x1 ^ y1, ... , xn ^ yn)

    """

    def __enc(self, key, block):
        return block ^ key

    def __init__(self, blocks):
        super().__init__(blocks)

    def __enc_block(self, key, start, end):
        for index in range(start, end + 1):
            #print("{}({})".format(index, index - start), end=" ")
            if index >= len(self.blocks):
                self.encblocks.append(0x00)
            else:

                block = self.blocks[index]
                self.encblocks[index] = self.__enc(key[index - start], block)

    def __transf(self, key):
        blocklen = len(key)
        textlen = len(self.blocks)
        padding = textlen % blocklen
        normslize = textlen + padding

        for index in range(0, normslize, blocklen):
            #print("blocks: {} {}".format(index, index + blocklen - 1))
            self.__enc_block(key, index, index + blocklen - 1)

        return self

    def encode(self, key):
        return self.__transf(key)

    def decode(self, key):
        return self.__transf(key)


class Transposition(object):

    def __init__(self, blocks):
        self.blocks = blocks
        self.encblocks = bytearray(self.blocks)

