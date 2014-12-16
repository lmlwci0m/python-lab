from .networkcommonserver import AbstractProtocolServer

__author__ = 'roberto'


class HttpProtocolServer(AbstractProtocolServer):

    ST_READY = 0

    def ready(self):
        pass

    def define_protocol(self):

        self.protocol = {
            self.ST_READY: self.ready
        }
