# ISIS
Python bindings for ISIS

### Setup

Usage of the library requires that ISIS be installed and that
`ISISROOT` is set. You can install ISIS using the conda environment
in that comes with this repo:

`conda env create -f environment.yml`

`conda activate isis`

Or use an existing ISIS installation.

You can then use `pip install -e .` to make the 
[console_scripts](./setup.py) available in your $PATH. These
scripts mimic the native executables that ship with ISIS. However,
since they're named the same, be aware that `pipe install -e .`
within the same conda environment or virtualenv as ISIS will 
overwrite the native binaries.

### Usage

[_load_isis()](./isis/isis.py) uses 
[cppyy](https://cppyy.readthedocs.io/en/latest/index.html) to lazily 
load `libisis.so` for the whole of the package. 

[include_isis()](./isis/isis.py) allows individual library functions
to include the proper headers to use `libisis.so`'s exports. 

### Examples

Here's what a very basic version of 
[isis2std](https://github.com/USGS-Astrogeology/ISIS3/blob/dev/isis/src/base/apps/isis2std/main.cpp)
looks as [a Python function](./isis/base/isis2std.py):

```python
from ..isis import include_isis

Isis = include_isis([
    "ExportDescription.h",
    "FileName.h",
    "ImageExporter.h",
    "UserInterface.h",
    "CubeAttribute.h",
    "FileName.h",
])


def isis2std(from_: str, to: str, fmt: str):
    # TODO: BITTYPE, MODE, QUALITY, COMPRESSION, STRETCH, MINIMUM, MAXIMUM
    bit_type = Isis.UnsignedByte
    mode = "grayscale"
    quality = 100
    compression = "none"
    minimum = 0.0
    maximum = 255.0

    print("From:   {}".format(from_))
    print("To:     {}".format(to))
    print("Format: {}\n".format(fmt))

    exporter = Isis.ImageExporter.fromFormat(fmt)

    exportDesc = Isis.ExportDescription()
    exportDesc.setPixelType(bit_type)

    from_attrs = Isis.CubeAttributeInput()
    from_attrs.setAttributes(Isis.FileName(from_))

    exportDesc.addChannel(from_, from_attrs)

    # Without this exporter.write() segfaults
    exportDesc.channel(0).setInputRange(-float("inf"), float("inf"))

    exporter.setGrayscale(exportDesc)

    output_file_name = Isis.FileName(to)
    exporter.write(output_file_name, quality, compression)

```

And then as a [console script](./isis/bin/base/isis2std.py):

```python
#!/usr/bin/env python3

from ...argparser import IsisArgParser
from ...base import isis2std


def main():
    args = IsisArgParser(description="Export an ISIS cube to one of several popular standard image formats")
    args.add_required("from", help="The ISIS cube to convert")
    args.add_required("to", help="The converted output file")
    args.add_required(
        "format",
        choices=("bmp", "jpeg", "jp2", "png", "tiff"),
        help="The output format"
    )
    args.parse()

    isis2std(args["from"], args["to"], args["format"])


if __name__ == "__main__":
    main()

```