from enum import Enum
from typing import Optional, Union

import cppyy
from cppyy import gbl

from ..isis import include_isis

Isis = include_isis([
    "Pvl.h"
])

cppyy.cppdef("""
namespace IsisUtils {
    std::string pvl_to_string(Isis::Pvl *pvl) {
        std::stringstream ss;
        ss << *pvl;
        return ss.str();
    }
    
    Isis::Pvl pvl_from_string(std::string str) {
        Isis::Pvl pvl;
        std::stringstream ss;
        
        ss << str;
        ss >> pvl;
        
        return pvl;
    }
}
""")

QString = gbl.QString
IsisUtils = gbl.IsisUtils


class Pvl:
    def __init__(self, file_path: str = None):
        if file_path is None:
            self._isis_pvl = Isis.Pvl()
        else:
            self._isis_pvl = Isis.Pvl(QString(file_path))

    @staticmethod
    def from_str(pvl_str: str):
        new_pvl = Pvl()
        new_pvl._isis_pvl = IsisUtils.pvl_from_string(pvl_str)
        return new_pvl

    def __str__(self):
        return str(IsisUtils.pvl_to_string(self._isis_pvl))

    def read_from_file(self, file_path: str):
        self._isis_pvl.read(QString(file_path))

    def write_to_file(self, file_path: str):
        self._isis_pvl.write(QString(file_path))

    def append(self, file_path: str):
        self._isis_pvl.append(QString(file_path))

    def set_format_template(self, templ_pvl_obj_or_str: Union[str, "Pvl"]):
        if isinstance(templ_pvl_obj_or_str, str):
            templ = QString(templ_pvl_obj_or_str)
        else:
            templ = templ_pvl_obj_or_str._isis_pvl
        self._isis_pvl.setFormatTemplate(templ)

    def terminator(self, terminator_str: str = None) -> Optional[str]:
        if terminator_str is not None:
            self._isis_pvl.setTerminator(QString(terminator_str))
        else:
            return str(self._isis_pvl.terminator().toUtf8().constData())

    @staticmethod
    def from_isis(pvl: Isis.Pvl):
        new_pvl = Pvl()
        new_pvl._isis_pvl = pvl
        return new_pvl
