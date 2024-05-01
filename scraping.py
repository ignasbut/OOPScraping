import time

import undetected_chromedriver as uc
from undetected_chromedriver import By
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from car import Car
import autogidas
import autoplius
import brc
from listing_class import Listing, ListingExtension


def prts(objects):
    print(f"Number of scraped objects: {len(objects)}")

    for obj in objects:
        print("--------------------------")
        obj.print_info()


# def decorator(brand, model, price_from=None, price_to=None, year_from=None, year_to=None,):
def decorator(src, *args):
    arr = []
    for arg in src:
        # tmp = arg.get_objects(brand, model, price_from, price_to, year_from, year_to)
        tmp = arg.get_objects(*args)
        for obj in tmp:
            arr.append(obj)
    return arr


def conv_obj(*args):
    vals = []
    for arg in args:
        if arg == '':
            vals.append(None)
        else:
            vals.append(arg)
    brand = vals[0]
    model = vals[1]
    year_from = vals[2]
    year_to = vals[3]
    sources = [autogidas, autoplius, brc]
    arr = decorator(sources, brand, model, None, None, year_from, year_to)
    # prts(arr) ; this is for printing
    return arr

# start()


# extended = listing_extension.from_listing(objects[1],"This is a description")

# TODO: Currently, the scraper scrapes the info and dumps it into an array.
#       Will have to integrate either serial dump into DB or by page in bulk.

# TODO: Create a function that takes the car class from car.py and sets it up as a
#       query to send over to the scraping tools

# TODO: Audogidas is mostly fully done in terms of what the functionality should be.
#       Ideally, it should be fully done with DB integration and query parsing
#       so that the rest of the websites are mostly copy-paste.
#       However, I think I should just start working on the foundations of the other websites, so
#       that everything can be seamlessly integrated.
#       A different option may be to leave them as is and create some intermediate file/function
#       that handles the storage.. Though that may be Armando's task.
