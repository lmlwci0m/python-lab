import os

__author__ = 'roberto'


ECLIPSE_PATH = 'D:\\progetti\\java_projects_eclipse_kepler\\eclipse_sr2\\'


class EclipseMgmt(object):

    def __init__(self, path=ECLIPSE_PATH):
        self.path = path

    def show_dirs(self):
        for entry in os.listdir(self.path):
            print(entry)


class EclipseProjectMgmt(object):

    def __init__(self, project_path):
        self.project_path = project_path
        self.java_source_path = os.path.join(self.project_path, "src", "main", "java")
        self.java_resources_path = os.path.join(self.project_path, "src", "main", "resources")

    def normalize_web(self):
        if not os.path.isdir(self.java_source_path):
            os.mkdir(self.java_source_path)


if __name__ == '__main__':

    webtools_path = "D:\\progetti\\java_projects_eclipse_kepler\\workspace_sr2\\webtools"
    EclipseProjectMgmt(webtools_path).normalize_web()

    #em = EclipseMgmt()
    #em.show_dirs()