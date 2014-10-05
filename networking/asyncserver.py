#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# asyncserver.py: implementation of a generic message passing
# asynchronous server using custom protocols.
#
# basic behaviour:
#
# <client>                  <server>
#
#   --------- [connect] -------->
#
#   <-- [send message length] ---
#   <----- [send message] -------
#
#   --- [send message length] -->
#   ------ [send message] ------>
#
#               ...
#
from abc import abstractmethod

import socket
import sys
import select

from networking import networkcommon

__author__ = 'roberto'


INADDR_ANY = ''
INADDR_BROADCAST = '<broadcast>'


class AbstractProtServer(networkcommon.AbstractProt):

    def __init__(self, client_socket, to_read, to_write, client_list, address):

        super(AbstractProtServer, self).__init__(client_socket)

        self.data_send = None
        self.data_recv = None

        self.to_read, self.to_write = to_read, to_write
        self.client_list, self.address = client_list, address

        self.define_protocol()


class Prot(AbstractProtServer):

    def status_0(self):
        print("start sending msglen")

        self.msg_send_init(self.get_strlen_bytes('WELCOME_MESSAGE'))  # message lenght in bytes

        msg = self.msg_next()  # First attempt to send message length
        if not self.msg_send(msg):  # self.sent < self.msglen:  # not finished
            self.status = 100
        else:  # finished
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)  # In both cases we need to write

    def status_100(self):
        print("continue sending msglen")

        msg = self.msg_next()  # Continue sending
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 100
        else:
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)

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
            close_connection(self.client_socket, self.client_list, self.address)

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
            close_connection(self.client_socket, self.client_list, self.address)

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


def close_connection(client_socket, client_list, address):
    print("Closing connection with {}".format(address))

    client_socket.close()
    client_list[address] = None
    del client_list[address]

    print("Closed connection with {}".format(address))


def main():

    print("Starting Asynchronous Communication Server...")

    selected_bind_addr = INADDR_ANY
    selected_bind_port = 8091
    selected_blocking_mode = False
    selected_backlog = 0
    selected_timeout = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        print("Server socket initialized")

        #
        # Connection listener initialization
        #
        server_socket.bind((selected_bind_addr, selected_bind_port))
        server_socket.setblocking(selected_blocking_mode)
        server_socket.listen(selected_backlog)

        print("Set server socket: binding to {}:{}, blocking mode: {}, backlog: {}".format(
            selected_bind_addr,
            selected_bind_port,
            selected_blocking_mode,
            selected_backlog
        ))

        #
        # Asynchronous management initialization
        #
        client_list = {}  # number of remote client connected
        protocol_instances = {}
        to_read = [server_socket]  # Only server socket for initial connection listening is set
        to_write = []
        to_err = []

        try:

            print("Starting server loop...")

            #
            # Single main loop: wait for everything
            #
            while True:

                #
                # Wait for available channels
                #

                ready_to_read, ready_to_write, in_error = select.select(to_read, to_write, to_err, selected_timeout)

                if server_socket in ready_to_read:

                    print("New connection.")

                    #
                    # Manage server_socket first: avoiding removal from to_read list
                    # (server_socket must always stay on to_read list)
                    #

                    ready_to_read.remove(server_socket)  # Gotcha: remove from ready_to_read list
                    # to_read.remove(server_socket)

                    try:

                        #
                        # New connection from remote host. Operations:
                        # - start connection
                        # - put connection on client list for exit management
                        # - put on "to write" list for the next loop
                        # - create protocol object
                        #

                        (client_socket, address) = server_socket.accept()
                        print("Getting connection from {}".format(address))
                        client_list[address] = client_socket
                        to_write.append(client_socket)  # the server must respond first (ex. hello message)
                        protocol_instances[client_socket] = Prot(client_socket, to_read, to_write, client_list, address)
                        print("Accepted connection from {}".format(address))

                    except BlockingIOError:  # Windows management
                        pass

                    except:
                        print("Unexpected error: {}".format(sys.exc_info()[0]))

                for client_socket in ready_to_read:
                    to_read.remove(client_socket)  # socket will be set for select by progress()
                    protocol_instances[client_socket].progress()

                for client_socket in ready_to_write:
                    to_write.remove(client_socket)  # socket will be set for select by progress()
                    protocol_instances[client_socket].progress()

                for client_socket in in_error:
                    pass  # TODO

        except KeyboardInterrupt:

            #
            # Pressing ctrl-c : closing all clients connections
            #

            print("shutdown: started by interrupt")
            for address in client_list:
                print("shutdown: closing connection with {}".format(address))
                client_list[address].close()
                print("shutdown: closed connection with {}".format(address))
            print("shutdown: closed all client connections")

    print("Server halted")


if __name__ == '__main__':
    main()