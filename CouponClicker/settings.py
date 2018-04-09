SAFEWAY_URL = "http://www.safeway.com"
LOGIN_URL = "https://www.safeway.com/iaaw/service/authenticate"
COUPONS_URL = "https://nimbus.safeway.com/J4UProgram1/services/program/CD/offer/allocations?details=y&hierarchies=y&notes=y"
COUPON_URL = "https://nimbus.safeway.com/J4UProgram1/services/offer/{offerID}/definition/cacheTs/{offerTS}"
CLIP_COUPON_URL = "https://nimbus.safeway.com/Clipping1/services/clip/items"

INITIAL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

INITIAL_COOKIES = {
    "SWY_API_KEY": "emjou",
    "SWY_BANNER": "safeway",
    "SWY_VERSION": "1.0"
}
