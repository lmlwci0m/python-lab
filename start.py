#!/usr/bin/env python

__author__ = 'roberto'

import __main__

import os

from mgmt.management import start_managerment_app

SCRIPT_DIR = os.path.dirname(__main__.__file__)


def main():

    app = start_managerment_app(SCRIPT_DIR)
    app.start_loop()


if __name__ == '__main__':
    main()