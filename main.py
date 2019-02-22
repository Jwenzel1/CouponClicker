import json
from configparser import ConfigParser

from couponclicker.commands import handle_args
from couponclicker.constants import CONFIG_FILE
from couponclicker.safeway import SafewayCoupons

if __name__ == "__main__":
    params = handle_args()
    if all([params.username, params.password]):
        username, password = params.username, params.password
    else:
        config = ConfigParser()
        config.read(CONFIG_FILE)
        username = config["safeway.com"]["username"]
        password = config["safeway.com"]["password"]
    s = SafewayCoupons(username, password)
    output = s.clip_all_coupons()
    print(json.dumps(output, indent=4))
