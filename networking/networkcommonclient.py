from . import networkcommon

__author__ = 'roberto'


class AbstractProtocolClient(networkcommon.AbstractProtocol):
    """General implementation of socket wrapper for initialization.

        General steps for receiving a message:

            Step 1: acquire message lenght
                expected_len = self.MSGLEN_FIELD_SZ

            Step 1 (ALT): acquire message lenght
                expected_len = self.data['MEG_LEN']

            Step 2: initialize buffer for message receiving
                self.init_recv_buffer(expected_len)

            Step 3 blocking receive
                while not self.msg_recv():
                    pass

            Step 4 (ALT): getting string data from buffer if needed
                self.data['MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)

            Step 4 (ALT): getting integer data from buffer if needed
                self.data['MSG_LEN'] = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)

    """

    def __init__(self, client_socket):
        """Only socket is wrapped."""

        super(AbstractProtocolClient, self).__init__(client_socket)

        self.define_protocol()