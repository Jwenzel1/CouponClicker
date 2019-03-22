from argparse import ArgumentParser

from couponclicker.settings import ARGPARSE_SETTIGNS, ARGS_SETTINGS, Arg


def handle_args():
    parser = ArgumentParser(
        description=ARGPARSE_SETTIGNS["description"],
        epilog=ARGPARSE_SETTIGNS["epilogue"],
    )
    parser.add_argument(
        ARGS_SETTINGS[Arg.CONFIG]["short"],
        ARGS_SETTINGS[Arg.CONFIG]["long"],
        help=ARGS_SETTINGS[Arg.CONFIG]["help"],
        default=ARGS_SETTINGS[Arg.CONFIG]["default"],
    )
    parser.add_argument(
        ARGS_SETTINGS[Arg.USER]["short"],
        ARGS_SETTINGS[Arg.USER]["long"],
        help=ARGS_SETTINGS[Arg.USER]["help"],
    )
    parser.add_argument(
        ARGS_SETTINGS[Arg.PASS]["short"],
        ARGS_SETTINGS[Arg.PASS]["long"],
        help=ARGS_SETTINGS[Arg.PASS]["help"],
    )

    return parser.parse_args()
