import subprocess
from javamgmt import environment
from javamgmt.classcreator import JavaMgmt

__author__ = 'roberto'



class CompilerLauncher(JavaMgmt):

    def __init__(self, cmd=environment.WIN_JAVA_8):
        self.cmd = cmd
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