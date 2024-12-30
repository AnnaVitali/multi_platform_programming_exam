""" Task definitions for invoke command line utility for python bindings
    overview article.
"""

import glob
import os
import pathlib
import re
import shutil
import sys
from setuptools import setup, Extension
import cffi
import invoke

on_win = sys.platform.startswith("win")
@invoke.task
def clean(c):
    """Remove any built objects"""
    for file_pattern in (
        "*.o",
        "*.so",
        "*.obj",
        "*.dll",
        "*.exp",
        "*.lib",
        "*.pyd",
        "cffi_example*",  # Is this a dir?
        "cython_wrapper.cpp",
    ):
        for file in glob.glob(file_pattern):
            os.remove(file)
    for dir_pattern in "Release":
        for dir in glob.glob(dir_pattern):
            shutil.rmtree(dir)


def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))


@invoke.task()
def build_library(c, path=None):
    """Build the shared library for the sample C code"""
    # Moving this type hint into signature causes an error (???)
    c: invoke.Context
    if on_win:
        if not path:
            print("Path is missing")
        else:
            # Using c.cd didn't work with paths that have spaces :/
            path = f'"{path}vcvars32.bat" x86'  # Enter the VS venv
            path += f'&& cd "{os.getcwd()}"'  # Change to current dir
            path += "&& cl /LD library.c"  # Compile
            # Uncomment line below, to suppress stdout
            # path = path.replace("&&", " >nul &&") + " >nul"
            c.run(path)
    else:
        print_banner("Building C Library")
        cmd = "gcc -c -Wall -Werror -fpic ./native/library.c -o ./native/library.o"
        invoke.run(cmd)
        invoke.run("gcc -shared -o ./native/liblibrary.so ./native/library.o")
        print("* Complete")
        
@invoke.task()
def test_ctypes(c):
    """Run the script to test ctypes"""
    print_banner("Testing ctypes Module for C")
    # pty and python3 didn't work for me (win).
    if on_win:
        invoke.run("python ctypes_test.py")
    else:
        invoke.run("python3 ctypes_test.py", pty=True)


@invoke.task(build_library)
def build_cffi(c):
    """Build the CFFI Python bindings"""
    print_banner("Building CFFI Module")
    ffi = cffi.FFI()

    this_dir = pathlib.Path().resolve()
    h_file_name = this_dir / "native" / "library.h"
    with open(h_file_name) as h_file:
        lines = h_file.read().splitlines()
        ffi.cdef("\n".join(lines))
    ffi.set_source(
        "library_cffi",
        '#include "library.h"',
        libraries=["library"],
        library_dirs=[(this_dir / "native").as_posix()],
        include_dirs=[(this_dir / "native").as_posix()],
        runtime_library_dirs=[(this_dir / "native").as_posix()],
    )

    ffi.compile(tmpdir=(this_dir / "native").as_posix())
    print("* Complete")


@invoke.task(build_cffi)
def test_cffi(c):
    """Run the script to test CFFI"""
    print_banner("Testing CFFI Module")
    invoke.run("python cffi_test.py", pty=not on_win)

@invoke.task()
def build_cython(c):
    """Compile a Python module from a C++ source file"""
    invoke.run("cython --cplus -3 library.pyx")
    if on_win:
        invoke.run('cl /LD /I "%INCLUDE%" library.cpp /Fe:library.pyd')
    else:
        # -fPIC $(python3-config --includes) is used to generate position-independent code and include Python headers
        invoke.run("g++ -shared -std=c++11 -fPIC $(python3-config --includes) -o library.so library.cpp")
    print("* Build complete")

