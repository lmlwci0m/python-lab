#!/usr/bin/env python

__author__ = 'roberto'

from mgmt.management import start_managerment_app


def main():
    app = start_managerment_app()
    app.start_loop()


if __name__ == '__main__':
    main()