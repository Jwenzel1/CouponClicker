from commands import handle_args
from SafewayAccount import SafewayAccount
from json import dumps

if __name__ == "__main__":
    args = handle_args()
    user, pword = args.user, args.pword
    acc = SafewayAccount(user, pword)
    print(dumps(acc.getCoupons(), indent=4))
    # clips = acc.clipAllCoupons()
    # print(f"Clipped {clips} coupons.")