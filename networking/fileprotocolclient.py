from .networkcommonclient import AbstractProtocolClient

__author__ = 'roberto'


class FileProtocolClient(AbstractProtocolClient):

    ST_READY_RECEIVE = 0

    ST_FILE_SEND = 1

    ST_END = 2

    def receive(self):

        expected_len = self.MSGLEN_FIELD_SZ

        self.init_recv_buffer(expected_len)

        while not self.msg_recv():
            pass

        self.data['MSG_LEN'] = int.from_bytes(self.databuffer, self.NETWORK_ENDIANNESS)

        expected_len = self.data['MSG_LEN']

        self.init_recv_buffer(expected_len)

        while not self.msg_recv():
            pass

        self.data['MESSAGE'] = str(self.databuffer, self.STRING_DEFAULT_ENCODING)

        print(self.data['MESSAGE'])

        self.status = self.ST_FILE_SEND

    def file_send(self):

        self.status = self.ST_END

    def define_protocol(self):

        self.protocol = {
            self.ST_READY_RECEIVE: self.receive,
            self.ST_FILE_SEND: self.file_send,
            self.ST_END: self.idle
        }