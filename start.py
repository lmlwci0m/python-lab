#!/usr/bin/env python
import logging.config

__author__ = 'roberto'

import __main__

import os

from mgmt.management import start_managerment_app
from mgmt.logconf import logging_conf

from commons.logging_utils import LoggingManager

SCRIPT_DIR = os.path.dirname(__main__.__file__)


def main():

    logging_manager = LoggingManager()

    logging_manager.init_logging(logging_conf)

    logger = logging_manager.get_logger(__name__)

    logger.info("Starting management app")

    app = start_managerment_app(SCRIPT_DIR, logging_manager)

    logger.debug("Started app. Starting loop")

    app.start_loop()

    logger.debug("Ending loop")

    logger.info("Ending management app")


if __name__ == '__main__':
    main()