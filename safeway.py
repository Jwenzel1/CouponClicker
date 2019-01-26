import json
from time import sleep

import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from constants import ClipStatuses

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
        driver.get("http://www.safeway.com")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("input-email").send_keys(self.username)
        driver.find_element_by_id("password-password").send_keys(self.password)
        driver.find_element_by_id("create-account-btn").click()
        sleep(3)
        store_id = driver.execute_script(
            'return window.localStorage.getItem("storeId")')
        access_token_info = driver.execute_script(
            'return window.localStorage.getItem("okta-token-storage")')
        access_token_info = json.loads(access_token_info)
        driver.quit()
        auth_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "X-swyConsumerDirectoryPro": access_token_info["access_token"]["accessToken"],
            "Authorization": f'Bearer {access_token_info["access_token"]["accessToken"]}'
        }
        store_id = store_id
        return auth_headers, store_id

    def get_coupons(self):
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
        return res.json().get("offers", [])

    def clip_coupon(self, coupon):
        result = {
            "status": None,
            "coupon_id": coupon['offerId'],
            "error": ""
        }
        if coupon["clipStatus"] == "U":
            print(f"Adding coupon: {coupon['offerId']}")
            payload = {
                "items": [
                    {
                        "clipType": "C",
                        "itemId": coupon["offerId"],
                        "itemType": coupon["offerPgm"],
                        "vndrBannerCd": ""
                        # I dont knoww where this value is found on the page or in
                        # cookies. It does not seem to matter though
                        # "vndrBannerCd": "" if coupon["offerPgm"] == "SC" else
                    },
                    {
                        "clipType": "L",
                        "itemId": coupon["offerId"],
                        "itemType": coupon["offerPgm"]
                    }
                ]
            }
            try:
                requests.post(
                    "https://nimbus.safeway.com/Clipping1/services/clip/items",
                    headers=self.auth_headers,
                    json=payload
                ).raise_for_status()
            except requests.HTTPError as exc:
                result["status"] = ClipStatuses.FAILED
                result["error"] = str(exc)
            else:
                result["status"] = ClipStatuses.ADDED
        else:
            result["status"] = ClipStatuses.SKIPPED
        return result

    def clip_all_coupons(self):
        coupons = self.get_coupons()
        results = {
            "total": len(coupons),
            "added": 0,
            "skipped": 0,
            "failed": 0,
            "failures": []
        }
        if not coupons:
            return results
        for coupon in coupons:
            result = self.clip_coupon(coupon)
            if result["status"] == ClipStatuses.ADDED:
                results["added"] += 1
            elif result["status"] == ClipStatuses.SKIPPED:
                results["skipped"] += 1
            else: #failed
                results["failures"].append({
                    "coupon_id": result["coupon_id"],
                    "error": result["error"]
                })
                # Don't continue. Don't want them to notice a bunch of errors.
                raise Exception(json.dumps(results, indent=4))
        results["failed"] = len(results["failures"])
        return results
