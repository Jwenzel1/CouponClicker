from argparse import ArgumentParser


def handle_args():
    parser = ArgumentParser(
        description="Activate all J4U offers in a Safeway account.",
        epilog="\n")
    parser.add_argument(
        "-u", "--username",
        help="The username of the account. Typically an email address.")
    parser.add_argument(
        "-p", "--password",
        help="The password for the account.")
    return parser.parse_args()
