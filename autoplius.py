website = 'https://autoplius.lt/paieska/naudoti-automobiliai'
root = 'https://autoplius.lt/'

xpaths = {
    "make_box": '//select[@id="make_id_list|]',
    "model_box": '//select[@id="make_id_sublist_portal"]',
    "price_from": '',
    "price_to": '',
    "year_from": '',
    "year_to": '',
    "body_type": '',
    "fuel_type": '',
    "adv_search": '',
    "but_submit": '',
    "paginator": '',
    "but_next": '',
    "list_container": '',
    "captcha_accept": '',
}

from seleniumbase import Driver
import time
from seleniumbase import Driver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bisect import bisect_left
from car import Listing, ListingExtension
import dbms

driver = Driver(uc=True, ad_block_on=True, headless=True)


def get_objects(*args):
    print("Autoplius will be scraped later")
    return []