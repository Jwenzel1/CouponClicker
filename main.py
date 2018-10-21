import json

from commands import handle_args
from safeway import SafewayCoupons

if __name__ == "__main__":
    params = handle_args()
    s = SafewayCoupons(params.username, params.password)
    output = s.clip_all_coupons()
    print(json.dumps(output, indent=4))
