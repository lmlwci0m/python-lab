from . import networkcommon

__author__ = 'roberto'


class AbstractProtocolServer(networkcommon.AbstractProtocol):
    """General implementation of socket wrapper for initialization.

        General steps for sending a message:

            Step 1: prepare message
                self.data["MESSAGE"] = "messaage content"

            Step 2: init message
                message_len_as_bytes = self.get_str_encoded("MESSAGE")
                self.msg_send_init(message_len_as_bytes)

            Step 2 (ALT): init message len
                message_as_bytes = self.get_str_len_encoded("MESSAGE")
                self.msg_send_init(message_as_bytes)

            Step 3: non blocking send
                msg = self.msg_next()
                if not self.msg_send(msg):
                    # continue
                else:
                    # finished

            Step 3 (ALT): blocking send
                msg = self.msg_next()
                while not self.msg_send(msg):
                    msg = self.msg_next()

            Step 4: request for write if needed
                self.to_write.append(self.client_socket)

            Step 4 (ALT): request for read if needed
                self.to_read.append(self.client_socket)

            Step 5: close connection if needed
                self.close_connection()

        General steps for receiving a message:

            Step 1: acquire message lenght
                expected_len = self.MSGLEN_FIELD_SZ

            Step 1 (ALT): acquire message lenght
                expected_len = self.data['MEG_LEN']

            Step 2: initialize buffer for message receiving
                self.init_recv_buffer(expected_len)

            Step 3: non blocking receive
                if not self.msg_recv():
                    # continue
                else:
                    # finished

            Step 3 (ALT): blocking receive
                while not self.msg_recv():
                    pass

            Step 4 (ALT): getting string data from buffer if needed
                self.data['MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)

            Step 4 (ALT): getting integer data from buffer if needed
                self.data['MSG_LEN'] = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)

            Step 5: request for write if needed
                self.to_write.append(self.client_socket)

            Step 5 (ALT): request for read if needed
                self.to_read.append(self.client_socket)

            Step 6: close connection if needed
                self.close_connection()

    """

    def __init__(self, client_socket, to_read, to_write, client_list, address):
        """For server purposes, the list of fd to read and write and
        the client list is set.
        """

        super(AbstractProtocolServer, self).__init__(client_socket)

        self.data_send = None
        self.data_recv = None

        self.to_read, self.to_write = to_read, to_write
        self.client_list, self.address = client_list, address

        self.define_protocol()

    def push_to_read(self):
        self.to_read.append(self.client_socket)

    def push_to_write(self):
        self.to_write.append(self.client_socket)

    def close_connection(self):
        print("Closing connection with {}".format(self.address))

        self.client_socket.close()
        self.client_list[self.address] = None
        del self.client_list[self.address]

        print("Closed connection with {}".format(self.address))