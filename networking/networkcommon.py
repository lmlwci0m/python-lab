__author__ = 'roberto'


class AbstractProtocol(object):

    STRING_DEFAULT_ENCODING = "utf-8"

    MSGLEN_FIELD_SZ = 4  # Default message lenght number of byte representation
    NETWORK_ENDIANNESS = 'big'  # Default endianness ('big' or 'little')
    #DEFAULT_RECV_SIZE = 8192

    def __init__(self, client_socket):
        """Initializes protocol.

            Start status is 0.
        """

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
        # Buffer used to receive data
        #
        self.databuffer = bytearray()

        #
        # Information specific of the protocol
        # can be used for storing data to be send or to be received
        #
        self.data = {}

        #
        # Status of the protocol
        #
        self.status = 0

    def progress(self):
        # here the socket must pe put on read or write queue for select()

        self.protocol[self.status]()

    def init_recv_buffer(self, expected_len):
        '''Initializes buffer for starting receving from remote endpoint.'''

        self.databuffer.clear()
        self.expected_len = expected_len

    def msg_recv(self):
        chunk = self.client_socket.recv(self.expected_len)
        self.databuffer.extend(chunk)
        self.expected_len -= len(chunk)
        return self.expected_len == 0

    def get_str_encoded(self, name):
        return self.data[name].encode(self.STRING_DEFAULT_ENCODING)

    def get_str_len_encoded(self, name):
        return len(self.get_str_encoded(name)).to_bytes(self.MSGLEN_FIELD_SZ, self.NETWORK_ENDIANNESS)
        #return len(self.data[name]).to_bytes(self.MSGLEN_FIELD_SZ, self.NETWORK_ENDIANNESS)

    def get_rcvd_msg_int(self):
        return int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)

    def get_rcvd_msg_str(self):
        return str(self.databuffer, self.STRING_DEFAULT_ENCODING)

    def idle(self):
        pass

    def msg_next(self):
        return self.message[self.sent:]

    def msg_send_init(self, msg_bytes):
        self.message = msg_bytes
        self.msglen = len(self.message)
        self.sent = 0

    def msg_send(self, msg):
        self.sent += self.client_socket.send(msg)
        return self.sent >= self.msglen