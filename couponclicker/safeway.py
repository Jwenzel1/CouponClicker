import json
from time import sleep
from typing import Tuple
from urllib.parse import unquote

import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from couponclicker.models import ClipCouponResponse, GetCouponsResponse, Offer


class SafewayCoupons(object):

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.access_token = ""
        self.user_agent = ""
        self.store_id = ""
        self.session = requests.Session()
        self.authenticate()
        # self.auth_headers, self.store_id = self.authenticate()

    @property
    def coupons_headers(self) -> dict:
        return {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-SWY_VERSION": "1.0",
            "X-SWY_BANNER": "safeway",
            "X-IBM-Client-Id": "306b9569-2a31-4fb9-93aa-08332ba3c55d",
            "X-IBM-Client-Secret": "N4tK3pW7pP6nB4kL6vN4kW0rS5lE4qH2fY0aB2rK1eP5gK4yV5",
            "Content-Type": "application/json",
            "X-SWY_API_KEY": "emjou",
            "DNT": "1",
            "X-swyConsumerDirectoryPro": self.access_token,
            "SWY_SSO_TOKEN": self.access_token,
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

    def authenticate(self):
        # Use selenium to perform the login and grab the token
        try:
            driver = webdriver.Chrome()
        except WebDriverException:
            print("Chrome not detected. Trying Firefox.")
            driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get("https://www.safeway.com")
        driver.find_element_by_id("myaccount-button").click()
        sleep(1)
        driver.find_element_by_id("linkToSignIn").click()
        driver.find_element_by_id("label-email").send_keys(self.username)
        driver.find_element_by_id("label-password").send_keys(self.password)
        driver.find_element_by_id("btnSignIn").click()
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "make-store")))
        except TimeoutException:
            print("The 'choose store' modal never appeared. I'm going to continue and assume everything is alright.")
        else:
            driver.find_element_by_css_selector("#make-store .make-store-btn").click()
        sleep(5)
        # print(json.dumps(driver.get_cookies(), indent=4, sort_keys=True))
        for cookie in driver.get_cookies():
            self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])
        token_dict = json.loads(unquote(self.session.cookies.get("SWY_SHARED_SESSION")))
        self.access_token = token_dict["accessToken"]
        coupons_info = json.loads(driver.execute_script('return localStorage.getItem("abCoupons")'))
        self.store_id = coupons_info["branchId"]
        # print(self.store_id)
        self.user_agent = driver.execute_script('return navigator.userAgent')
        driver.close()

    def get_coupons(self) -> list:
        try:
            res = self.session.get(
                "https://www.safeway.com/abs/pub/web/j4u/api/offers/gallery",
                params={
                    "storeId": self.store_id,
                    "offerPgm": "PD-CC"
                },
                headers=self.coupons_headers)
            res.raise_for_status()
        except requests.HTTPError:
            print(f"Failed to get coupons. Response has this content: {res.content}")
            raise
        coupons = res.json()
        # print(json.dumps(coupons, indent=4))
        return coupons["PD"] + coupons["CC"]


    def clip_coupon(self, coupon: dict) -> bool:
        output = False
        if coupon["status"] == "U":
            print(f"Adding coupon: {coupon['offerId']} | {coupon.get('offerPrice', '')} {coupon.get('description', '')} {coupon.get('name', '')}")
            payload = {
                "items": [
                    {
                        "clipType": "C",
                        "itemId": coupon["offerId"],
                        "itemType": coupon["offerPgm"],
                    },
                    {
                        "clipType": "L",
                        "itemId": coupon["offerId"],
                        "itemType": coupon["offerPgm"],
                    }
                ]
            }
            try:
                res = self.session.post(
                    "https://www.safeway.com/abs/pub/web/j4u/api/offers/clip",
                    params={"storeId": self.store_id},
                    headers=self.coupons_headers,
                    json=payload
                )
                res.raise_for_status()
            except requests.HTTPError:
                # I may add some error handling here later but for now just
                # throw the error
                raise
            else:
                output = True
        return output

    def clip_all_coupons(self) -> Tuple[int, int, int]:
        total, added, skipped = 0, 0, 0
        for coupon in self.get_coupons():
            result = self.clip_coupon(coupon)
            total += 1
            if result:
                added += 1
            else:
                skipped += 1
        return total, added, skipped
