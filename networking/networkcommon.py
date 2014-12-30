import struct

__author__ = 'roberto'

import types


class AbstractProtocol(object):
    """Low level operations for asynchronous socket communications."""

    STRING_DEFAULT_ENCODING = "utf-8"

    MSGLEN_FIELD_SZ = 4  # Default message lenght number of byte representation
    NETWORK_ENDIANNESS = 'big'  # Default endianness ('big' or 'little')
    #DEFAULT_RECV_SIZE = 8192

    def __init__(self, main_location, client_socket, initial_status=0):
        """Initializes protocol.

            Start status is 0.
        """

        #
        # Propagation of "current script directory"
        #
        self.main_location = main_location

        #
        # Socket instance to remote endpoint
        #
        self.client_socket = client_socket

        #
        # Information for message sending
        #
        self.message = "".encode(self.STRING_DEFAULT_ENCODING)
        self.msglen = len(self.message)
        self.sent = 0

        #
        # Buffer used to receive data and intial handler set as None
        #
        self.databuffer = bytearray()
        self.handler = None

        #
        # Information specific of the protocol
        # can be used for storing data to be send or to be received
        #
        self.data = {}

        #
        # Status of the protocol and initial dummy protocol definition
        #
        self.status = initial_status
        self.protocol = {self.status: self.idle}

    def progress(self):
        """Executes the next step of the protocol according to the current status."""

        # here the socket must pe put on read or write queue for select()

        self.protocol[self.status]()

    def clear_databuffer(self):
        """Initializes buffer for data receiving."""

        try:
            self.databuffer.clear()
        except AttributeError as e:
            self.databuffer = bytearray()

    def __expected_len_handler(self, chunk):

        return self.expected_len == 0

    def init_recv_buffer(self, expected_len, handler=None):
        """Initializes buffer for starting receving from remote endpoint.
            Parameters:
                expected_len: sets the number of bytes to be received from remote endpoint.
        """

        if handler:
            self.handler = types.MethodType(handler, self)
        else:
            self.handler = self.__expected_len_handler

        self.clear_databuffer()
        self.expected_len = expected_len

    def msg_recv(self):
        """Receives data from socket.
            Return value:
                True if the expected number of bytes has been received. False otherwise.
        """

        chunk = self.client_socket.recv(self.expected_len)
        self.databuffer.extend(chunk)
        self.expected_len -= len(chunk)
        return self.handler(chunk)

    def get_str_encoded(self, name):
        """Returns the encoded value of data[name]."""

        encoded_str = self.data[name].encode(self.STRING_DEFAULT_ENCODING)
        return encoded_str

    def get_str_len_encoded(self, name):
        """Returns the MSGLEN_FIELD_SZ-byte encoded value of the lenght of the encoded value of data[name]."""

        encoded = self.get_str_encoded(name)
        encoded_len = len(encoded)
        try:
            return encoded_len.to_bytes(self.MSGLEN_FIELD_SZ, self.NETWORK_ENDIANNESS)
        except AttributeError as e:
            return struct.pack(">i", encoded_len)

    def get_rcvd_msg_int(self):
        """Get the value of databuffer content as integer using NETWORK_ENDIANNESS."""

        try:
            return int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)
        except AttributeError as e:
            return struct.unpack(">i", self.databuffer)[0]

    def get_rcvd_msg_str(self):
        """Get the value of databuffer content as string using STRING_DEFAULT_ENCODING."""

        try:
            return str(self.databuffer, self.STRING_DEFAULT_ENCODING)
        except TypeError as e:
            return unicode(self.databuffer)

    def idle(self):
        pass

    def msg_next(self):
        """Get the next chunk for message to be sent."""

        return self.message[self.sent:]

    def msg_send_init(self, msg_bytes):
        """Intializes a message for sending."""

        self.message = msg_bytes
        self.msglen = len(self.message)
        self.sent = 0

    def msg_send(self, msg):
        """Send msg to remote endpoint."""

        self.sent += self.client_socket.send(msg)
        return self.sent >= self.msglen
