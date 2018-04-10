from json import dumps
from requests import Session

from settings import (
    CLIP_COUPON_URL, COUPONS_URL, COUPON_URL, INITIAL_COOKIES,
    INITIAL_HEADERS, LOGIN_URL, SAFEWAY_URL)


class SafewayAccount(object):
    """Object representation of a Safeway account."""

    def __init__(self, uname, pword):
        """Constructs an authenticated account object."""
        self.uname = uname
        self.pword = pword
        self.session = Session()
        self.session.headers.update(INITIAL_HEADERS)
        self.session.cookies.update(INITIAL_COOKIES)
        self._getCookie()
        self._authenticate()

    def _getCookie(self):
        """Get the session cookie for the account.
        
        Safeway sets a cookie in your browser when you go to
        www.safeway.com. This cookie is used for authentication and
        also contains additional information needed for getting
        coupons.
        """
        self.session.get(SAFEWAY_URL)

    def _authenticate(self):
        """Log into www.safeway.com.
        
        Performs the actual log in to the user's account.
        """
        payload = {
            "password": self.pword,
            "rememberMe": False,
            "source": "WEB",
            "userId": self.uname
        }
        self.session.post(LOGIN_URL, json=payload)

    def getCoupons(self):
        """Get a list of all coupons in the account.
        
        Calls Safewayy's endpoint for populating the j4u coupons. This
        returns all coupons in a convenient list.
        
        Example Output: 
        [
            {
                "offerId": 8049186,
                "offerPgm": "MF",
                "offerSubPgm": "09",
                "offerProvider": "couponsinc",
                "offerTs": 1523111403000,
                "clipStatus": "C",
                "listStatus": "S",
                "purchaseInd": "L",
                "offerDetail": {
                    "offerStartDt": "\\/Date(1523199600000)\\/",
                    "offerEndDt": "\\/Date(1525532400000)\\/",
                    "purchaseRank": 1,
                    "arrivalRank": 47,
                    "expiryRank": 47
                }
            }
        ]
        """
        cookies = self.session.cookies.get_dict()
        headers = {
            "X-SWY_API_KEY": INITIAL_COOKIES["SWY_API_KEY"],
            "X-SWY_BANNER": INITIAL_COOKIES["SWY_BANNER"],
            "X-SWY_VERSION": INITIAL_COOKIES["SWY_VERSION"],
            "X-swyConsumerDirectoryPro": cookies["swyConsumerDirectoryPro"],
            "X-swyConsumerlbcookie": cookies["swyConsumerlbcookie"]
        }
        res = self.session.get(COUPONS_URL, headers=headers)
        return res.json().get("offers", [])

    def getCouponById(self, offerID: int, offerTS: int):
        """Get coupon details given the offerID and offerTS
        
        This returns a single coupon given it's offerId and offerTS.
        The only way to get offerID and offerTS is to call
        getCoupons and find the coupon you want.

        Example Output:
        {
            "offerId": 8598573,
            "offerPgm": "MF",
            "imageId": "207/619207_c014e593-f8bb-4389-a425-ec7a79d...",
            "usageType": "O",
            "priceType": "CO",
            "offerStartDt": "\\/Date(1522605600000)\\/",
            "offerEndDt": "\\/Date(1524938400000)\\/",
            "offerStartDate": "2018-04-01",
            "offerEndDate": "2018-04-28",
            "offerTs": "1523111418000",
            "offerProvider": "couponsinc",
            "vndrBannerCd": "2bbf4b36-a75e-11e6-80f5-76304dec7eb7#C",
            "extlOfferId": "00052-138085-00",
            "hierarchies": {
                "categories": [
                    "16"
                ],
                "events": [
                    "524"
                ]
            },
            "offerSubPgm": "09",
            "offerDetail": {
                "primaryCategoryNM": "Paper, Cleaning & Home",
                "titleDsc1": "Gain",
                "prodDsc1": "on ONE Gain Sheets 105 ct or higher (...",
                "savingsValue": "Save $2.00",
                "disclaimer": "Dealer: Submission to Procter & Gam...",
                "offerCategoryTypeCd": ""
            }
        }
        """
        url = COUPON_URL.format(offerID=offerID, offerTS=offerTS)
        res = self.session.get(url)
        return res.json()

    def clipCoupon(self, coupon):
        cookies = self.session.cookies.get_dict()
        headers = {
            "X-SWY_API_KEY": INITIAL_COOKIES["SWY_API_KEY"],
            "X-SWY_BANNER": INITIAL_COOKIES["SWY_BANNER"],
            "X-SWY_ISREMEMBERED": "False",
            "X-SWY_VERSION": INITIAL_COOKIES["SWY_VERSION"],
            "X-swyConsumerDirectoryPro": cookies["swyConsumerDirectoryPro"],
            "X-swyConsumerlbcookie": cookies["swyConsumerlbcookie"]
        }
        payload = {
            "items": [
                {
                    "clipType": "C",
                    "itemId": coupon["offerId"],
                    "itemType": coupon["offerPgm"],
                    "vndrBannerCd": ""
                    # "vndrBannerCd": "" if coupon["offerPgm"] == "SC" else
                },
                {
                    "clipType": "L",
                    "itemId": coupon["offerId"],
                    "itemType": coupon["offerPgm"]
                }
            ]
        }
        self.session.post(CLIP_COUPON_URL, headers=headers, json=payload)

    def clipAllCoupons(self):
        coupons = self.getCoupons()
        clips = 0
        for coupon in coupons:
            if coupon["clipStatus"] == "U":
                self.clipCoupon(coupon)
                clips += 1
        return clips