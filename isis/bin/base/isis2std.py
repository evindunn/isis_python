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
