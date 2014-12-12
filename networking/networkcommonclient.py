from networking import networkcommon

__author__ = 'roberto'


class AbstractProtClient(networkcommon.AbstractProt):
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

            Step 3: blocking send
                msg = self.msg_next()
                while not self.msg_send(msg):
                    msg = self.msg_next()

    """

    def __init__(self, client_socket):
        """Only socket is wrapped."""

        super(AbstractProtClient, self).__init__(client_socket)

        self.define_protocol()