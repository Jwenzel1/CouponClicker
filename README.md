# CouponClicker
Accept Safeway J4U offers

## Running
This project uses pipenv for installing and managing dependencies although the only dependency is requests. To install all required dependencies, make sure you have pipenv installed first with 

`pip install pipenv` 

then create a virtualenv and install dependencies with

`pipenv install`

If you run into issues you may not have python 3.6 installed on your system which is required.
Afterwards you can run the program with

`pipenv run python CouponClicker/main.py -u <email> -p <password>`
