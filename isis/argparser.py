from sys import argv
from typing import List, Dict, Type
from os.path import basename


class _InvalidFormatException(Exception):
    pass


class _MissingRequiredArgException(Exception):
    pass


class _UnknownArgException(Exception):
    pass


class _InvalidArgTypeException(Exception):
    pass


class _InvalidArgValueException(Exception):
    pass


class _IsisArg:
    def __init__(self, help: str, type: Type, choices: List):
        super().__init__()
        self.help = help
        self.type = type
        self.choices = choices


class IsisArgParser(dict):
    def __init__(self, description=""):
        super().__init__()
        self._description = description
        self._required_args: Dict[str, _IsisArg] = dict()
        self._optional_args: Dict[str, _IsisArg] = dict()

    def add_required(self, key: str, help="", type=str, choices=None):
        self._required_args[key.strip("-")] = _IsisArg(help, type, choices)

    def add_optional(self, key: str, help="", type=str, choices=None):
        self._optional_args[key.strip("-")] = _IsisArg(help, type, choices)

    def usage(self):
        usage_str = "{}\n\n".format(self._description)
        usage_str += "Usage: {} [...arg=val arg=val]\n".format(basename(argv[0]))

        if len(self._required_args) > 0:
            usage_str += "Required Arguments:\n"
            for k, v in self._required_args.items():
                usage_str += "\t{}={}".format(k, v.type.__name__).ljust(10)
                if v.help != "":
                    usage_str += "\t{}".format(v.help)
                usage_str += "\n"

        if len(self._optional_args) > 0:
            usage_str += "\nOptional Arguments:\n"
            for k, v in self._optional_args.items():
                usage_str += "\t{}={}\n".format(k, v.type.__name__).ljust(10)
                if v.help != "":
                    usage_str += "\t{}".format(v.help)
                    usage_str += "\n"

        return usage_str

    def parse(self):
        try:
            self._parse()
        except Exception as e:
            print("\nERROR: {}\n".format(e))
            self._usage_and_exit()

    def _usage_and_exit(self):
        print(self.usage())
        exit(1)

    def _parse(self):
        registered_args = (
            list(self._required_args.keys()) +
            list(self._optional_args.keys())
        )

        args = argv[1:]
        parsed_args = dict()

        for arg in args:
            if arg in ["-h", "--help"]:
                self._usage_and_exit()

            try:
                k, v = arg.split("=")
                k = k.strip("-")
            except ValueError:
                raise _InvalidFormatException(
                    "Invalid argument: {}".format(arg)
                )

            if k not in registered_args:
                raise _UnknownArgException("Unknown argument: {}".format(k))
            elif k in self._required_args.keys():
                registered_arg = self._required_args[k]
            else:
                registered_arg = self._optional_args[k]

            try:
                parsed_args[k] = registered_arg.type(v)
            except ValueError:
                raise _InvalidArgTypeException(
                    "{} must be a {}".format(k, registered_arg.type.__name__)
                )

            if registered_arg.choices is not None and v not in registered_arg.choices:
                raise _InvalidArgValueException(
                    "{} must be one of {}".format(
                        k,
                        ", ".join([str(a) for a in registered_arg.choices])
                    )
                )

            parsed_args[k] = v

        parsed_arg_keys = parsed_args.keys()
        for arg in self._required_args.keys():
            if arg not in parsed_arg_keys:
                raise _MissingRequiredArgException("{} is required".format(arg))

        self.update(parsed_args)
