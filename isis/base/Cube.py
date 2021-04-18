import cppyy

from .Pvl import Pvl
from ..isis import include_isis
from os.path import exists as path_exists

Isis = include_isis([
    "Cube.h",
    "FileName.h"
])

QString = cppyy.gbl.QString


class Cube:
    FMT_BSQ = Isis.Cube.Format.Bsq
    FMT_TILE = Isis.Cube.Format.Tile

    def __init__(self, file_name: str = None, access: str = "r"):
        if file_name is not None:
            if not path_exists(file_name):
                raise FileNotFoundError("{} does not exist!".format(file_name))

            self._isis_cub = Isis.Cube(
                Isis.FileName(file_name),
                QString(access)
            )
        else:
            self._isis_cub = Isis.Cube()

    def close(self, remove=False):
        return self._isis_cub.close(remove)

    def is_open(self) -> bool:
        return self._isis_cub.isOpen()

    def is_projected(self) -> bool:
        return self._isis_cub.isProjected()

    def is_read_only(self) -> bool:
        return self._isis_cub.isReadOnly()

    def is_read_write(self) -> bool:
        return self._isis_cub.isReadWrite()

    def labels_attached(self) -> bool:
        return self._isis_cub.labelsAttached()

    def band_count(self) -> int:
        return self._isis_cub.bandCount()

    def label(self) -> Pvl:
        return Pvl.from_isis(self._isis_cub.label())

    def base(self) -> float:
        return self._isis_cub.base()

    def byte_order(self) -> int:
        return self._isis_cub.byteOrder()

    def external_cube_file_name(self) -> str:
        return str(self._isis_cub.externalCubeFileName().toUtf8().constData())

    def file_name(self) -> str:
        return str(self._isis_cub.fileName().toUtf8().constData())

    def label_size(self, actual=False) -> int:
        return self._isis_cub.labelSize(actual)

    def line_count(self) -> int:
        return self._isis_cub.lineCount()

    def multiplier(self) -> float:
        return self._isis_cub.multiplier()

    def sample_count(self) -> int:
        return self._isis_cub.sampleCount()

    def stores_dn_data(self) -> bool:
        return self._isis_cub.storesDnData()

    def has_group(self, group_name: str) -> bool:
        return self._isis_cub.hasGroup(QString(group_name))

    def has_table(self, table_name: str) -> bool:
        return self._isis_cub.hasTable(QString(table_name))

    def has_blob(self, blob_name: str, blob_type: str) -> bool:
        return self._isis_cub.hasBlob(QString(blob_name), QString(blob_type))

    @staticmethod
    def from_isis(cube: Isis.Cube):
        new_cub = Cube()
        new_cub._isis_cub = cube
        return new_cub
