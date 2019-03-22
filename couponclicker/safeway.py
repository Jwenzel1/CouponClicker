import json
from time import sleep
from typing import Tuple

import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from couponclicker.models import ClipCouponResponse, GetCouponsResponse, Offer


class SafewayCoupons(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth_headers, self.store_id = self.authenticate()

    def authenticate(self):
        # Use selenium to perform the login and grab the token
        try:
            driver = webdriver.Chrome()
        except WebDriverException:
            print("Chrome not detected. Trying Firefox.")
            driver = webdriver.Firefox()
        driver.get("https://www.safeway.com")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("input-email").send_keys(self.username)
        driver.find_element_by_id("password-password").send_keys(self.password)
        driver.find_element_by_id("create-account-btn").click()
        sleep(3)
        store_id = driver.execute_script(
            'return window.localStorage.getItem("storeId")')
        access_token_info = driver.execute_script(
            'return window.localStorage.getItem("okta-token-storage")')
        user_agent = driver.execute_script('return navigator.userAgent')
        driver.quit()
        access_token_info = json.loads(access_token_info)
        access_token = access_token_info["access_token"]["accessToken"]
        auth_headers = {
            "User-Agent": user_agent,
            "X-swyConsumerDirectoryPro": access_token,
            "Authorization": f"Bearer {access_token}"
        }
        return auth_headers, store_id

    def get_coupons(self) -> GetCouponsResponse:
        params = {
            "_dc": 1537665638533, # Dunno what this value does but we need it
            "details": "y",
            "hierarchies": "y",
            "notes": "y",
            "storeId": self.store_id
        }
        res = requests.get(
            f"https://nimbus.safeway.com/J4UProgram1/services/program/CD/offer/allocations",
            headers=self.auth_headers,
            params=params)
        return GetCouponsResponse.deserialize(res.json())

    def clip_coupon(self, coupon: Offer) -> ClipCouponResponse:
        output = None
        if coupon.clipStatus == "U":
            print(f"Adding coupon: {coupon.offerId}")
            payload = {
                "items": [
                    {
                        "clipType": "C",
                        "itemId": coupon.offerId,
                        "itemType": coupon.offerPgm,
                        "vndrBannerCd": ""
                        # I dont knoww where this value is found on the page or in
                        # cookies. It does not seem to matter though
                        # "vndrBannerCd": "" if coupon.offerPgm == "SC" else
                    },
                    {
                        "clipType": "L",
                        "itemId": coupon.offerId,
                        "itemType": coupon.offerPgm
                    }
                ]
            }
            try:
                res = requests.post(
                    "https://nimbus.safeway.com/Clipping1/services/clip/items",
                    headers=self.auth_headers,
                    json=payload
                )
                res.raise_for_status()
            except requests.HTTPError as exc:
                # I may add some error handling here later but for now just
                # throw the error
                raise
            else:
                output = ClipCouponResponse.deserialize(res.json())
        return output

    def clip_all_coupons(self) -> Tuple[int, int, int]:
        total, added, skipped = 0, 0, 0
        coupons = self.get_coupons()
        for coupon in coupons.offers:
            result = self.clip_coupon(coupon)
            total += 1
            if result:
                added += 1
            else:
                skipped += 1
        return total, added, skipped
