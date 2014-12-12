from networking.networkcommonclient import AbstractProtClient

__author__ = 'roberto'


class MessageProtocolClient(AbstractProtClient):

    def status_0(self):

        expected_len = self.MSGLEN_FIELD_SZ  #PROTOCOL_MESSAGE_LEN_FIELD_LEN

        self.init_recv_buffer(expected_len)

        print("Start receiving message len")
        while not self.msg_recv():
            pass

        expected_len = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)

        print("Received message len: {}".format(expected_len))

        self.init_recv_buffer(expected_len)

        print("Start receiving message")
        while not self.msg_recv():
            pass

        self.data['WELCOME_MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)

        print("Received message: {}".format(self.data['WELCOME_MESSAGE']))

        self.status = 1

    def status_1(self):

        # self.data['CLIENT_HELLO'] = 'test per vedere se invia il messaggio correttamente'

        self.data['CLIENT_HELLO'] = input("Scrivi il messaggio da inviare: ")

        self.msg_send_init(self.get_str_len_encoded('CLIENT_HELLO'))  # message lenght in bytes

        msg = self.msg_next()  # First attempt to send message length
        print("Start sending message len: {}".format(self.get_str_len_encoded('CLIENT_HELLO')))
        while not self.msg_send(msg):  # self.sent < self.msglen:  # not finished
            msg = self.msg_next()

        print("Sent message len")

        self.msg_send_init(self.get_str_encoded('CLIENT_HELLO'))

        msg = self.msg_next()  # First attempt to send message
        print("Start sending message: {}".format(msg))
        while not self.msg_send(msg):  # self.sent < self.msglen:  # not finished
            msg = self.msg_next()

        print("Sent message")

        self.status = 2

    def define_protocol(self):

        self.protocol = {
            0: self.status_0,
            1: self.status_1,
            2: self.idle}