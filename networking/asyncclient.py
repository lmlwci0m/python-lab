#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# asynclient.py: tester for asyncserver.py

import socket
import sys

from networking import networkcommon
from networking.messageprotocolclient import MessageProtocolClient
from networking.networkcommonclient import AbstractProtClient

__author__ = 'roberto'


def main():

    selected_remote_host = '127.0.0.1'
    selected_remote_port = 8081
    selected_end_protocol_status = 2

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        print("Client socket initialized. Estabilishing connection with {}:{}".format(selected_remote_host, selected_remote_port))

        try:

            client_socket.connect((selected_remote_host, selected_remote_port))

            try:

                print("Estabilished connection with {}".format(selected_remote_host))

                #
                # Wrapping socket into the ProtClient structure
                #
                prot = MessageProtocolClient(client_socket)

                #
                # Applying the protocol until end...
                #
                while prot.status != selected_end_protocol_status:
                    prot.progress()

                print("Client side protocol execution terminated successfully. Shutting down...")

                #
                # Shutting down connection
                #
                client_socket.shutdown(socket.SHUT_RDWR)

            except:
                print("Unexpected error: {}".format(sys.exc_info()[0]))

        except ConnectionRefusedError:
            print("Connection refused by {}".format(selected_remote_host))

    print("Closed connection to {}".format(selected_remote_host))


if __name__ == '__main__':
    main()