#!/usr/bin/env python3

from argparse import ArgumentParser
from ...base import isis2std


def main():
    parser = ArgumentParser(description="Export an ISIS cube to one of several popular standard image formats")
    parser.add_argument("from", help="The ISIS cube to convert")
    parser.add_argument("to", help="The converted output file")
    parser.add_argument(
        "format",
        choices=("bmp", "jpeg", "jp2", "png", "tiff"),
        help="The output format"
    )
    args = vars(parser.parse_args())

    isis2std(args["from"], args["to"], args["format"])


if __name__ == "__main__":
    main()
