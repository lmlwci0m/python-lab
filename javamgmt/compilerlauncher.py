import subprocess
from javamgmt.classcreator import JavaMgmt

__author__ = 'RPANCALD'


class CompilerLauncher(JavaMgmt):

    cmd = "c:\\Program Files\\Java\\jdk1.8.0\\bin\\javac.exe"

    def __init__(self):
        super(CompilerLauncher, self).__init__()

    def compile_class(self, filepath):
        args = [self.cmd, filepath]
        returncode = subprocess.call(args)
        return returncode

    def compile_classes(self, classes):
        args = [self.cmd]
        args.extend(classes)
        returncode = subprocess.call(args)
        return returncode


if __name__ == '__main__':

    classfile = "d:\\progetti\\javaworks\\org\\crynet\\crypto\\BaseCryptoClass.java"

    CompilerLauncher().compile_class(classfile)