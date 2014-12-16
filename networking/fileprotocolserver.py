from .networkcommonserver import AbstractProtocolServer

__author__ = 'roberto'


class FileProtocolServer(AbstractProtocolServer):

    ST_READY_MSG_LEN = 0
    ST_READY_MSG_LEN_CONTINUE = 100

    ST_READY_MSG = 1
    ST_READY_MSG_CONTINUE = 200

    ST_RECEIVE_NAME_LEN = 2
    ST_RECEIVE_NAME_LEN_CONTINUE = 300

    ST_RECEIVE_NAME = 3
    ST_RECEIVE_NAME_CONTINUE = 400

    ST_RECEIVE_LEN = 4
    ST_RECEIVE_LEN_CONTINUE = 500

    ST_RECEIVE = 5
    ST_RECEIVE_CONTINUE = 600

    ST_DONE = 6

    def send_ready_len(self):
        """ server --- send welcome message length --> client """

        self.msg_send_init(self.get_str_len_encoded('READY_MSG'))

        self.status = self.ST_READY_MSG_LEN_CONTINUE

        self.push_to_write()

    def send_ready_len_continue(self):
        """ server --- send welcome message length --> client """

        if not self.msg_send(self.msg_next()):
            self.status = self.ST_READY_MSG_LEN_CONTINUE
        else:
            self.status = self.ST_READY_MSG

        self.push_to_write()

    def send_ready(self):
        """ server --- send welcome message --> client """

        self.msg_send_init(self.get_str_encoded('READY_MSG'))

        self.status = self.ST_READY_MSG_CONTINUE

        self.push_to_write()

    def send_ready_continue(self):
        """ server --- send welcome message --> client """

        if not self.msg_send(self.msg_next()):
            self.status = self.ST_READY_MSG_CONTINUE
            self.push_to_write()
        else:
            self.status = self.ST_RECEIVE_NAME_LEN
            self.push_to_read()

    def receive_name_lenght(self):
        """ client --- receive file length --> server"""

        self.init_recv_buffer(self.MSGLEN_FIELD_SZ)

        self.status = self.ST_RECEIVE_NAME_LEN_CONTINUE

        self.push_to_read()

    def receive_name_lenght_continue(self):
        """ client --- receive file length --> server"""

        if not self.msg_recv():
            self.status = self.ST_RECEIVE_NAME_LEN_CONTINUE
        else:
            self.data['MSG_LEN'] = self.get_rcvd_msg_int()
            self.status = self.ST_RECEIVE_NAME

        self.push_to_read()

    def receive_name(self):

        self.init_recv_buffer(self.data['MSG_LEN'])

        self.status = self.ST_RECEIVE_NAME_CONTINUE

        self.push_to_read()

    def receive_name_continue(self):

        if not self.msg_recv():
            self.status = self.ST_RECEIVE_NAME_CONTINUE
        else:
            self.data['FILE_NAME'] = self.get_rcvd_msg_str()
            self.status = self.ST_RECEIVE_LEN

        self.push_to_read()

    def receive_file_lenght(self):
        """ client --- receive file length --> server"""

        self.init_recv_buffer(self.MSGLEN_FIELD_SZ)

        self.status = self.ST_RECEIVE_LEN_CONTINUE

        self.push_to_read()

    def receive_file_lenght_continue(self):
        """ client --- receive file length --> server"""

        if not self.msg_recv():
            self.status = self.ST_RECEIVE_LEN_CONTINUE
        else:
            self.data['MSG_LEN'] = self.get_rcvd_msg_int()
            self.status = self.ST_RECEIVE

        self.push_to_read()

    def receive_file(self):

        self.init_recv_buffer(self.data['MSG_LEN'])

        self.status = self.ST_RECEIVE_CONTINUE

        self.push_to_read()

    def receive_file_continue(self):

        if not self.msg_recv():
            self.status = self.ST_RECEIVE_CONTINUE
            self.push_to_read()
        else:
            self.write_file(self.get_rcvd_msg_str())
            self.status = self.ST_DONE
            self.close_connection()

    def write_file(self, data):
        with open(self.data['FILE_NAME'], "w") as f:
            f.write(data)

    def define_protocol(self):

        self.data['READY_MSG'] = "Ready"

        self.protocol = {
            self.ST_READY_MSG_LEN: self.send_ready_len,
            self.ST_READY_MSG_LEN_CONTINUE: self.send_ready_len_continue,
            self.ST_READY_MSG: self.send_ready,
            self.ST_READY_MSG_CONTINUE: self.send_ready_continue,
            self.ST_RECEIVE_NAME_LEN: self.receive_name_lenght,
            self.ST_RECEIVE_NAME_LEN_CONTINUE: self.receive_name_lenght_continue,
            self.ST_RECEIVE_NAME: self.receive_name,
            self.ST_RECEIVE_NAME_CONTINUE: self.receive_name_continue,
            self.ST_RECEIVE_LEN: self.receive_file_lenght,
            self.ST_RECEIVE_LEN_CONTINUE: self.receive_file_lenght_continue,
            self.ST_RECEIVE: self.receive_file,
            self.ST_RECEIVE_CONTINUE: self.receive_file_continue,
            self.ST_DONE: self.idle
        }