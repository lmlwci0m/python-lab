__author__ = 'roberto'

import os
from utils.objects import UtilsFactory


if __name__ == '__main__':

    env = UtilsFactory.create_environment()

    env.show_all()