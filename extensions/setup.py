#!/usr/bin/env python3

from distutils.core import setup, Extension
import os
import shutil


EXTENSIONS_BUILD_DIR = "/Users/robertopancaldi/PycharmProjects/python-lab/extensions/build"
LIB_DIR = "lib.macosx-10.6-intel-3.4"
TEMP_DIR = "temp.macosx-10.6-intel-3.4"


def remove_all():
    os.remove(os.path.join(EXTENSIONS_BUILD_DIR, LIB_DIR, "blocks.so"))
    os.remove(os.path.join(EXTENSIONS_BUILD_DIR, TEMP_DIR, "blocks.o"))
    os.remove(os.path.join(EXTENSIONS_BUILD_DIR, TEMP_DIR, "utils.o"))
    os.rmdir(os.path.join(EXTENSIONS_BUILD_DIR, LIB_DIR))
    os.rmdir(os.path.join(EXTENSIONS_BUILD_DIR, TEMP_DIR))
    os.rmdir(EXTENSIONS_BUILD_DIR)


C_MODULES_LIST = ['blocks.c', 'utils.c']
MOD = 'blocks'
setup(name=MOD, ext_modules=[Extension(MOD, sources=C_MODULES_LIST)])

lib_build_path = os.path.abspath("./build/lib.macosx-10.6-intel-3.4")

lib_name = "blocks.so"

lib_full_path = os.path.join(lib_build_path, lib_name)

shutil.copyfile(lib_full_path, lib_name)

remove_all()
