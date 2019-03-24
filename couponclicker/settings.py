from enum import Enum, auto
from textwrap import dedent


class Arg(Enum):
    CONFIG = auto()
    USER = auto()
    PASS = auto()


ARGS_SETTINGS = {
    "REQUIRED": {"short", "long"},
    Arg.CONFIG: {
        "short": "-c",
        "long": "--config",
        "help": "Path to the config.ini file that contains the username and " \
                "password to use for safeway.com",
        "default": "config.ini"
    },
    Arg.USER: {
        "short": "-u",
        "long": "--username",
        "help": "The username of the account. Typically an email address.",
        "default": None
    },
    Arg.PASS: {
        "short": "-p",
        "long": "--password",
        "help": "The password for the account.",
        "default": None
    }
}


ARGPARSE_SETTIGNS = {
    "description": dedent("""
        Activate all J4U offers in a Safeway account.

        By default, searches for a config.ini file in the root of the project
        that contains creds for your safeway account. You can specify the
        location of the config file with the -c parameter.

        You can also pass in your username and password via the
        commandline using the -u and -p arguments."""),
    "epilogue": "\n"
}
