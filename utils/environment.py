import os
from utils.objects import UtilsFactory

__author__ = 'roberto'


if __name__ == '__main__':

    env = UtilsFactory.create_environment()

    env.show_all()