from argparse import ArgumentParser

from couponclicker.settings import ARGPARSE_SETTIGNS, ARGS_SETTINGS, Arg


def handle_args():
    parser = ArgumentParser(
        description=ARGPARSE_SETTIGNS["description"],
        epilog=ARGPARSE_SETTIGNS["epilogue"],
    )
    for a in Arg:
        options = {}
        for k, v in ARGS_SETTINGS[a].items():
            if k not in ARGS_SETTINGS["REQUIRED"]:
                options[k] = v
        parser.add_argument(
            ARGS_SETTINGS[a]["short"],
            ARGS_SETTINGS[a]["long"],
            **options
        )
    return parser.parse_args()
