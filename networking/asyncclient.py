#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# asynclient.py: tester for asyncserver.py

import socket
import sys

__author__ = 'roberto'

PROTOCOL_MESSAGE_LEN_FIELD_LEN = 4
NETWORK_ENDIANNESS = 'big'
DEFAULT_RECV_SIZE = 8192


def main():
    remote_host = '127.0.0.1'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        try:

            client_socket.connect((remote_host, 8091))
            try:
                print("Estabilished connection with {}".format(remote_host))

                data = bytearray()

                while not len(data) >= PROTOCOL_MESSAGE_LEN_FIELD_LEN:
                    chunk = client_socket.recv(DEFAULT_RECV_SIZE)
                    data.extend(chunk)

                data_len = int.from_bytes(data, NETWORK_ENDIANNESS)

                print(data_len)

                data = bytearray()
                while not len(data) >= data_len:
                    chunk = client_socket.recv(DEFAULT_RECV_SIZE)
                    data.extend(chunk)

                message = str(data, "utf-8")

                print(message)

                client_socket.shutdown(socket.SHUT_RDWR)

            except:
                print("Unexpected error: {}".format(sys.exc_info()[0]))

        except ConnectionRefusedError:
            print("Connection refused by {}".format(remote_host))

    print("Closed connection to {}".format(remote_host))


if __name__ == '__main__':
    main()