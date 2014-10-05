#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# asynclient.py: tester for asyncserver.py

import socket
import sys

from networking import networkcommon

__author__ = 'roberto'


class ProtClient(networkcommon.AbstractProt):

    def __init__(self, client_socket):

        super(ProtClient, self).__init__(client_socket)

        self.define_protocol()

    def status_0(self):

        expected_len = self.MSGLEN_FIELD_SZ #PROTOCOL_MESSAGE_LEN_FIELD_LEN

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

        self.data['CLIENT_HELLO'] = 'test per vedere se invia il messaggio correttamente'

        self.msg_send_init(self.get_strlen_bytes('CLIENT_HELLO'))  # message lenght in bytes

        msg = self.msg_next()  # First attempt to send message length
        print("Start sending message len: {}".format(self.get_strlen_bytes('CLIENT_HELLO')))
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


def main():
    remote_host = '127.0.0.1'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        try:

            client_socket.connect((remote_host, 8091))
            try:
                print("Estabilished connection with {}".format(remote_host))

                prot = ProtClient(client_socket)

                while prot.status != 2:
                    prot.progress()

                client_socket.shutdown(socket.SHUT_RDWR)

            except:
                print("Unexpected error: {}".format(sys.exc_info()[0]))

        except ConnectionRefusedError:
            print("Connection refused by {}".format(remote_host))

    print("Closed connection to {}".format(remote_host))


if __name__ == '__main__':
    main()