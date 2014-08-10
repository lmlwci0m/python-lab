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


MSGLEN_FIELD_SZ = 4  # Default message lenght number of byte representation
BYTE_ENDIANNESS = 'big'  # Default endianness ('big' or 'little')
DEFAULT_RECV_SIZE = 8192
INADDR_ANY = ''
INADDR_BROADCAST = '<broadcast>'


class AbstractProtServer(object):

    def idle(self):
        pass

    #def msg_first(self):
    #    return self.message

    def msg_next(self):
        return self.message[self.sent:]

    def msg_init(self, msg_bytes):
        self.message = msg_bytes
        self.msglen = len(self.message)
        self.sent = 0

    def msg_send(self, msg):
        self.sent += self.client_socket.send(msg)
        return self.sent >= self.msglen

    def __init__(self, client_socket, to_read, to_write, client_list, address):
        self.client_socket = client_socket
        self.data_send = None
        self.data_recv = None
        self.status = 0
        self.sent = 0
        self.to_read, self.to_write = to_read, to_write
        self.client_list, self.address = client_list, address

        self.message = "".encode("utf-8")
        self.msglen = len(self.message)

        self.define_protocol()

    def progress(self):
        # here the socket must pe put on read or write queue for select()

        self.protocol[self.status]()


class Prot(AbstractProtServer):

    def status_0(self):
        print("start sending msglen")

        # self.message = len("Ready").to_bytes(MSGLEN_FIELD_SZ, BYTE_ENDIANNESS)  # message lenght in bytes
        # self.msglen = len(self.message)

        self.msg_init(len("Ready").to_bytes(MSGLEN_FIELD_SZ, BYTE_ENDIANNESS))  # message lenght in bytes
        #msg = self.msg_first()  # First attempt to send message length

        msg = self.msg_next()  # First attempt to send message length
        # self.sent += self.client_socket.send(self.message) # First attempt to send message length
        #self.sent += self.client_socket.send(msg)
        if not self.msg_send(msg):  # self.sent < self.msglen:  # not finished
            self.status = 100
        else:  # finished
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)  # In both cases we need to write

    def status_100(self):
        print("continue sending msglen")

        msg = self.msg_next()  # Continue sending
        # self.sent += self.client_socket.send(self.message[self.sent:])  # Continue sending
        # self.sent += self.client_socket.send(msg)
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 100
        else:
            print("sent msglen")
            self.status = 1

        self.to_write.append(self.client_socket)

    def status_1(self):
        print("start sending message")
        # self.message = "Ready".encode("utf-8")
        # self.msglen = len(self.message)
        # self.sent += self.client_socket.send(self.message)
        self.msg_init("Ready".encode("utf-8"))

        msg = self.msg_next()
        if not self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 200
            self.to_write.append(self.client_socket)
        else:
            print("sent message")
            self.status = 2
            close_connection(self.client_socket, self.client_list, self.address)

    def status_200(self):
        print("continue sending message")
        # self.sent += self.client_socket.send(self.message[self.sent:])

        msg = self.msg_next()
        if not  self.msg_send(msg):  # self.sent < self.msglen:
            self.status = 200
            self.to_write.append(self.client_socket)
        else:
            print("sent message")
            self.status = 2
            close_connection(self.client_socket, self.client_list, self.address)

    def define_protocol(self):

        self.protocol = {
            0: self.status_0,
            100: self.status_100,
            1: self.status_1,
            200: self.status_200,
            2: self.idle}


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
        client_list = {}
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
                        to_write.append(client_socket)
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