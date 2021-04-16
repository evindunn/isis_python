from typing import List
from os import getenv, environ as os_environ
from os.path import join as path_join

import cppyy
import cppyy.ll


def load_isis(headers: List[str]):
    conda_prefix = getenv("CONDA_PREFIX", None)

    if conda_prefix is None:
        raise RuntimeError("CONDA_PREFIX is not set")

    if getenv("ISISROOT", None) is None:
        os_environ["ISISROOT"] = conda_prefix

    cppyy.add_include_path(path_join(conda_prefix, "include"))
    cppyy.add_include_path(path_join(conda_prefix, "include", "isis"))
    cppyy.add_include_path(path_join(conda_prefix, "include", "cspice"))
    cppyy.add_include_path(path_join(conda_prefix, "include", "qt"))
    cppyy.add_include_path(path_join(conda_prefix, "include", "qt", "QtCore"))
    cppyy.add_include_path(path_join(conda_prefix, "include", "qt", "QtWidgets"))

    cppyy.add_library_path(path_join(conda_prefix, "lib"))

    with cppyy.ll.signals_as_exception():
        for file in headers:
            if not cppyy.include(file):
                raise Exception("Failed to load {}!".format(file))

    cppyy.load_library("isis")
    return cppyy.gbl.Isis
