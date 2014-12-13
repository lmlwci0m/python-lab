from .networkcommonserver import AbstractProtocolServer

__author__ = 'roberto'


class MessageProtocolServer(AbstractProtocolServer):

    def status_0(self):
        """WELCOME_MESSAGE is set by define_protocol().
        - get it as bytes
        - start sending:
            - if all bytes are sent: status 1 ()
            - else: status 100 (continue sending bytes)
        """

        print("start sending msglen")

        self.msg_send_init(self.get_str_len_encoded('WELCOME_MESSAGE'))  # message lenght in bytes

        msg = self.msg_next()  # First attempt to send message length
        if not self.msg_send(msg):  # self.sent < self.msglen:  # not finished
            self.status = 100
        else:  # finished
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)  # In both cases we need to write

    def status_100(self):
        """All bytes are not yet sent.
        - continue sending:
            - if all bytes are sent: status 1 (done)
            - else: status 100 (continue sending bytes)
        """

        print("continue sending msglen")

        msg = self.msg_next()  # Continue sending
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 100
        else:
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)  # In both cases we need to write

    def status_1(self):
        print("start sending message")

        self.msg_send_init(self.get_str_encoded('WELCOME_MESSAGE'))

        msg = self.msg_next()
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 200
            self.to_write.append(self.client_socket)
        else:
            print("sent message")
            self.status = 2
            self.to_read.append(self.client_socket)  # pass to receive from remote endpoint

    def status_200(self):
        print("continue sending message")

        msg = self.msg_next()
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 200
            self.to_write.append(self.client_socket)
        else:
            print("sent message")
            self.status = 2
            self.to_read.append(self.client_socket)  # pass to receive from remote endpoint

    def status_2(self):
        print("start receiving message len")

        expected_len = self.MSGLEN_FIELD_SZ

        self.init_recv_buffer(expected_len)
        if not self.msg_recv():
            self.status = 300
        else:
            print("received msglen")
            self.data['MSG_LEN'] = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)
            self.status = 3

        self.to_read.append(self.client_socket)  # in both cases we need to read

    def status_300(self):
        print("Continue receiving message len")

        if not self.msg_recv():
            self.status = 300
        else:
            print("received msglen")
            self.data['MSG_LEN'] = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)
            self.status = 3

        self.to_read.append(self.client_socket)  # in both cases we need to read

    def status_3(self):
        print("Start receiving message")

        expected_len = self.data['MSG_LEN']

        self.init_recv_buffer(expected_len)
        if not self.msg_recv():
            self.status = 400
            self.to_read.append(self.client_socket)
        else:
            print("received message")
            self.data['MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)
            self.status = 4
            print("Message is: {}".format(self.data['MESSAGE']))
            self.close_connection()

    def status_400(self):
        print("Continue receiving message")

        if not self.msg_recv():
            self.status = 400
            self.to_read.append(self.client_socket)
        else:
            print("received message")
            self.data['MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)
            self.status = 4
            print("Message is: {}".format(self.data['MESSAGE']))
            self.close_connection()

    def define_protocol(self):

        self.data['WELCOME_MESSAGE'] = "Welcome to asynchronous server."

        self.protocol = {
            0: self.status_0,
            100: self.status_100,
            1: self.status_1,
            200: self.status_200,
            2: self.status_2,
            300: self.status_300,
            3: self.status_3,
            400: self.status_400,
            4: self.idle}