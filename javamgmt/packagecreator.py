import os
from javamgmt.classcreator import JavaMgmt, ClassCreatorPackage
from javamgmt.compilerlauncher import CompilerLauncher

__author__ = 'roberto'


class PackageCreator(JavaMgmt):

    def __init__(self, basepath, packagename):

        super(PackageCreator, self).__init__()
        self.basepath = basepath
        self.packagename = packagename
        self.packagepath = None
        self.classes = []

    def get_packagepath(self):
        return self.packagepath

    def create(self):
        currentpath = self.basepath
        for dirname in self.packagename.split("."):
            newdir = os.path.join(currentpath, dirname)
            if not os.path.exists(newdir):
                print("Creating {0:s}".format(newdir))
                os.mkdir(newdir)
            currentpath = os.path.join(currentpath, dirname)
        self.packagepath = currentpath

    def load(self):
        currentpath = self.basepath
        for dirname in self.packagename.split("."):
            currentpath = os.path.join(currentpath, dirname)
        self.packagepath = currentpath


class PackageManager(JavaMgmt):

    def __init__(self, basepath):

        super(PackageManager, self).__init__()
        self.basepath = basepath
        self.packages = {}

    def create_package(self, packagename):
        self.packages[packagename] = PackageCreator(self.basepath, packagename)
        self.packages[packagename].create()

    def load_package(self, packagename):
        self.packages[packagename] = PackageCreator(self.basepath, packagename)
        self.packages[packagename].load()

    def add_class(self, classname, modifier, packagename):
        packagepath = self.packages[packagename].get_packagepath()
        classfile = ClassCreatorPackage(classname, modifier, packagename)
        classfile.create(packagepath)
        self.packages[packagename].classes.append(classfile.name)

    def load_class(self, classname, modifier, packagename):
        classfile = ClassCreatorPackage(classname, modifier, packagename)
        self.packages[packagename].classes.append(classfile.name)

    @staticmethod
    def create_structure(manager, packages):
        for packagename in packages.keys():
            manager.create_package(packagename)
            for classfile in packages[packagename]:
                manager.add_class(classfile, "public", packagename)

    @staticmethod
    def load_structure(manager, packages):
        for packagename in packages.keys():
            manager.load_package(packagename)
            for classfile in packages[packagename]:
                manager.load_class(classfile, "public", packagename)

    @classmethod
    def load_project(cls, basepath, packages):
        manager = PackageManager(basepath)
        PackageManager.load_structure(manager, packages)
        return manager

    @classmethod
    def create_project(cls, basepath, packages):
        manager = PackageManager(basepath)
        PackageManager.create_structure(manager, packages)
        return manager

    def build_all(self):
        classes = []
        for package in self.packages.keys():
            for classname in self.packages[package].classes:
                classfilepath = os.path.join(self.packages[package].packagepath, classname) + ".java"
                classes.append(classfilepath)
        retcode = CompilerLauncher().compile_classes(classes)


if __name__ == '__main__':
    pass
