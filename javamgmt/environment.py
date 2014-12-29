__author__ = 'roberto'

import os
from utils.objects import UtilsFactory


WIN_JAVA_7 = "c:\\Program Files\\Java\\jdk1.7.0_51\\bin\\javac.exe"
WIN_JAVA_8 = "c:\\Program Files\\Java\\jdk1.8.0\\bin\\javac.exe"


if __name__ == '__main__':

    env = UtilsFactory.create_environment()

    env.show_java()