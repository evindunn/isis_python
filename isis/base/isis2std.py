from ..isis import load_isis


Isis = load_isis([
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
