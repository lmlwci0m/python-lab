__author__ = 'roberto'


logging_conf = {

    'version': 1,

    'formatters': {

        'file_formatter': {
            'format': '[%(msecs)3d] %(asctime)s [%(levelname)8s] %(module)21s(%(lineno)4d) %(funcName)20s: %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },

        'stream_formatter': {
            'format': '[%(levelname)s]: %(message)s'
        }

    },

    'handlers': {

        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file_formatter',
            'level': 'INFO',
            'filename': 'mgmt.log',
            'maxBytes': 1024
        },

        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'stream_formatter',
            'level': 'INFO'
        },

        'file_handler_debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file_formatter',
            'level': 'DEBUG',
            'filename': 'mgmt.log',
            'maxBytes': 1024
        },

        'stream_handler_debug': {
            'class': 'logging.StreamHandler',
            'formatter': 'stream_formatter',
            'level': 'DEBUG'
        }

    },

    'root': {
        'level': 'DEBUG',
        'handlers': ['file_handler_debug', 'stream_handler_debug']
    }

}