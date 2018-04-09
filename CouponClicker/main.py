from CouponClicker.commands import handle_args
from CouponClicker.SafewayAccount import SafewayAccount

if __name__ == "__main__":
    args = handle_args()
    user, pword = args.user, args.pword
