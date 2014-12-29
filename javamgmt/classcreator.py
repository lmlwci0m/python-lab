__author__ = 'roberto'

import os


class JavaMgmt(object):
    def __init__(self):
        pass


class ClassCreator(JavaMgmt):

    @staticmethod
    def _apply_template(templatepath, destpath, *args):
        with open(templatepath) as template:
            with open(destpath + ".java", "w") as f:
                f.write(template.read().format(*args))

    def __init__(self, name):
        super(ClassCreator, self).__init__()
        self.name = name

    def create(self, destdir):
        self._apply_template("templates/classbasetemplate.java",
                             os.path.join(destdir, self.name), self.name)


class ClassCreatorExtended(ClassCreator):

    def __init__(self, name, modifier):
        super(ClassCreatorExtended, self).__init__(name)
        self.modifier = modifier

    def create(self, destdir):
        self._apply_template("templates/classmodtemplate.java",
                             os.path.join(destdir, self.name), self.name, self.modifier)


class ClassCreatorPackage(ClassCreatorExtended):

    def __init__(self, name, modifier, packagename):
        super(ClassCreatorPackage, self).__init__(name, modifier)
        self.packagename = packagename

    def create(self, destdir):
        self._apply_template("templates/classpacktemplate.java",
                             os.path.join(destdir, self.name), self.name, self.modifier, self.packagename)

if __name__ == '__main__':
    ClassCreator("TestClass").create(os.getcwd())
    ClassCreatorExtended("TestClassMod", "public").create(os.getcwd())
    packagepath = "D:\\progetti\\javaworks\\org\\crynet\\crypto"
    ClassCreatorPackage("TestClassPackage", "public", "org.crynet.crypto").create(packagepath)