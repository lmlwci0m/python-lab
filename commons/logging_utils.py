__author__ = 'roberto'

import logging.config


class LoggingManager(object):
    """Wrapper for logging library. All loggers are managed by an internal dictionary."""

    def __init__(self):
        """Initlaizes an empty logger."""

        self.registered_loggers = {}
        self.initialized = False
        self.logger = None

    def init_logging(self, dict_config):
        """Start initlialization of logging using a Python dictionary object."""

        if not self.initialized:
            logging.config.dictConfig(dict_config)
            self.logger = logging.getLogger(__name__)
            self.initialized = True
            self.logger.debug("LoggingManager initialized")

        else:
            self.logger.debug("LoggingManager already initialized")

    def get_logger(self, name):
        """Get logger for specified name. Creates it if not exists."""

        if name not in self.registered_loggers:
            self.logger.debug("{} not in registered logger. It will be initialized".format(name))
            self.registered_loggers[name] = logging.getLogger(name)

        return self.registered_loggers[name]
