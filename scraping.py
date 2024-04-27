import time

import undetected_chromedriver as uc
from undetected_chromedriver import By
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from car import Car
from autogidas import main as get_objects
from listing_class import listing, listing_extension

# TODO: Instead of generating custom URL, just use the search function via the website itself.
# This will make it easier to actually make the search queries
# As of now, only AUTOPLIUS can take in user-defined input, but AUTOGIDAS will need navigation via JS
# However, AUTOGIDAS has a more reasonable and text-based search for URL generation


objects = get_objects("Dodge")

print(f"Number of scraped objects: {len(objects)}")

for i in range(len(objects)):
    print(f"\n{i+1}. Make: {objects[i].make}\nModel: {objects[i].model}\n")