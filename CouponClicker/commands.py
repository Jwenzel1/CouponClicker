from argparse import ArgumentParser

def handle_args():
    parser = ArgumentParser(
        description="Activate all J4U offers in a Safeway account.",
        epilog="\n")
    parser.add_argument(
        '-u', '--user',
        help="The username of the account. Typically an email address.",
        metavar="",
        required=True)
    parser.add_argument(
        '-p', '--pword',
        help='The password for the account.',
        metavar="",
        required=True)
    return parser.parse_args()
