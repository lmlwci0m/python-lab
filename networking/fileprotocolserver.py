from networking.networkcommonserver import AbstractProtServer

__author__ = 'roberto'


class FileProtocolServer(AbstractProtServer):

    ST_READY_MSG_LEN = 0
    ST_READY_MSG_LEN_CONTINUE = 100

    ST_READY_MSG = 1
    ST_READY_MSG_CONTINUE = 200

    ST_RECEIVE = 2

    def send_ready_len(self):

        message = self.get_str_len_encoded('READY_MSG')
        self.msg_send_init(message)

        msg = self.msg_next()
        if not self.msg_send(msg):
            self.status = self.ST_READY_MSG_LEN_CONTINUE
        else:
            self.status = self.ST_READY_MSG

        self.push_to_write()

    def send_ready_len_continue(self):

        msg = self.msg_next()
        if not self.msg_send(msg):
            self.status = self.ST_READY_MSG_LEN_CONTINUE
        else:
            self.status = self.ST_READY_MSG

        self.push_to_write()

    def send_ready(self):

        message = self.get_str_encoded('READY_MSG')
        self.msg_send_init(message)

        msg = self.msg_next()
        if not self.msg_send(msg):
            self.status = self.ST_READY_MSG_CONTINUE
            self.push_to_write()
        else:
            self.status = self.ST_RECEIVE
            self.push_to_read()

    def send_ready_continue(self):

        msg = self.msg_next()
        if not self.msg_send(msg):
            self.status = self.ST_READY_MSG_CONTINUE
            self.push_to_write()
        else:
            self.status = self.ST_RECEIVE
            self.push_to_read()

    def define_protocol(self):

        self.data['READY_MSG'] = "Ready"

        self.protocol = {
            self.ST_READY_MSG_LEN: self.send_ready_len,
            self.ST_READY_MSG_LEN_CONTINUE: self.send_ready_len_continue,
            self.ST_READY_MSG: self.send_ready,
            self.ST_READY_MSG_CONTINUE: self.send_ready_continue,
            self.ST_RECEIVE: self.idle
        }