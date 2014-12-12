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
from networking.messageprotocolserver import MessageProtocolServer

__author__ = 'roberto'


INADDR_ANY = ''
INADDR_BROADCAST = '<broadcast>'


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
        to_read = [server_socket]  # Setting only server socket for initial connection listening
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
                        #
                        # Wrapping and mapping socket to a new Prot instance
                        #
                        protocol_instances[client_socket] = MessageProtocolServer(client_socket, to_read, to_write, client_list, address)
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