import os

__author__ = 'roberto'


ECLIPSE_PATH = 'D:\\progetti\\java_projects_eclipse_kepler\\eclipse_sr2\\'


class EclipseMgmt(object):

    def __init__(self, path=ECLIPSE_PATH):
        self.path = path

    def show_dirs(self):
        for entry in os.listdir(self.path):
            print(entry)


if __name__ == '__main__':

    em = EclipseMgmt()
    em.show_dirs()