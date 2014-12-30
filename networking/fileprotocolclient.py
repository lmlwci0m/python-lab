import sys
from .networkcommonclient import AbstractProtocolClient
from .inputwrapper import consoleinput

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

        self.data['MSG_LEN'] = self.get_rcvd_msg_int()

        expected_len = self.data['MSG_LEN']

        self.init_recv_buffer(expected_len)

        while not self.msg_recv():
            pass

        self.data['MESSAGE'] = self.get_rcvd_msg_str()

        print(self.data['MESSAGE'])

        self.status = self.ST_FILE_SEND

    def file_send(self):

        self.data['MESSAGE'] = consoleinput("Scrivi il nome della risorsa: ")

        self.msg_send_init(self.get_str_len_encoded('MESSAGE'))

        msg = self.msg_next()
        while not self.msg_send(msg):
            msg = self.msg_next()

        self.msg_send_init(self.get_str_encoded('MESSAGE'))

        msg = self.msg_next()
        while not self.msg_send(msg):
            msg = self.msg_next()

        self.data['MESSAGE'] = consoleinput("Scrivi il messaggio da inviare: ")

        self.msg_send_init(self.get_str_len_encoded('MESSAGE'))

        msg = self.msg_next()
        while not self.msg_send(msg):
            msg = self.msg_next()

        self.msg_send_init(self.get_str_encoded('MESSAGE'))

        msg = self.msg_next()
        while not self.msg_send(msg):
            msg = self.msg_next()

        self.status = self.ST_END


    def define_protocol(self):

        self.protocol = {
            self.ST_READY_RECEIVE: self.receive,
            self.ST_FILE_SEND: self.file_send,
            self.ST_END: self.idle
        }