import json
from configparser import ConfigParser
from textwrap import dedent

from couponclicker.commands import handle_args
from couponclicker.safeway import SafewayCoupons

if __name__ == "__main__":
    params = handle_args()
    if all([params.username, params.password]):
        username, password = params.username, params.password
    else:
        config = ConfigParser()
        config.read(params.config)
        username = config["safeway.com"]["username"]
        password = config["safeway.com"]["password"]
    s = SafewayCoupons(username, password)
    # s.get_coupons()
    total, added, skipped = s.clip_all_coupons()
    print("\n".join([
        f"Total = {total}",
        f"Added = {added}",
        f"Skipped = {skipped}"]))
    input("Press ENTER to exit.")
