from typing import List
from os import getenv, environ as os_environ
from os.path import join as path_join

import cppyy

_ENV_CONDA_PREFIX = "CONDA_PREFIX"
_ENV_ISIS_ROOT = "ISISROOT"


def _load_isis():
    isis_prefix = getenv(_ENV_ISIS_ROOT, None)

    if isis_prefix is None:
        isis_prefix = getenv(_ENV_CONDA_PREFIX, None)
        os_environ["ISISROOT"] = isis_prefix

    if isis_prefix is None:
        raise RuntimeError("{} is not set".format(_ENV_ISIS_ROOT))

    cppyy.add_include_path(path_join(isis_prefix, "include"))
    cppyy.add_include_path(path_join(isis_prefix, "include", "isis"))
    cppyy.add_include_path(path_join(isis_prefix, "include", "cspice"))
    cppyy.add_include_path(path_join(isis_prefix, "include", "qt"))
    cppyy.add_include_path(path_join(isis_prefix, "include", "qt", "QtCore"))
    cppyy.add_include_path(path_join(isis_prefix, "include", "qt", "QtWidgets"))

    cppyy.add_library_path(path_join(isis_prefix, "lib"))

    cppyy.load_library("isis")


def include_isis(headers: List[str]):
    for file in headers:
        if not cppyy.include(file):
            raise Exception("Failed to load {}!".format(file))

    return cppyy.gbl.Isis
