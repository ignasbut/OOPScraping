import time
from seleniumbase import Driver
# import selenium.webdriver.chrome.options -- most likely not needed
from selenium.webdriver.support.ui import Select
# import undetected_chromedriver as uc -- this is probably useless now
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bisect import bisect_left
from listing_class import listing, listing_extension


driver = Driver(uc=True, ad_block_on=True, headless=True)
website = 'https://autogidas.lt/en/paieska/automobiliai'
root = 'https://autogidas.lt/'


def pinfo(*args):
    print("[*] ", *args)


def perror(*args):
    print("[!] ", *args)


def psuccess(*args):
    print("[+] ", *args)


# XPaths of the website search and listings
xpaths = {
    "make_box": '//div[@id="f_1"]',
    "model_box": '//div[@id="f_model_14"]',
    "price_from": '//select[@id="f_215"]',
    "price_to": '//select[@id="f_216"]',
    "year_from": '//select[@id="f_41"]',
    "year_to": '//select[@id="f_42"]',
    "body_type": '',
    "fuel_type": '',
    "adv_search": '',
    "but_submit": '//button[@id="submit-button"]',
    "paginator": '//div[@class="paginator"]',
    "but_next": '//a[contains(div, "Next")]/div',
    "list_container": './/main/article',
    "captcha_accept": '//button[@id="onetrust-accept-btn-handler"]',
}

# Relative XPaths of the individual values within an individual listing
relative_xpaths = {
    "link": './/a[@class="item-link "]',
    "year": './/span[contains(@class,"param-year")]/b',
    "fuel": './/span[contains(@class,"param-fuel-type")]/b',
    "mileage": './/span[contains(@class,"param-mileage")]/b',
    "gearbox": './/span[contains(@class,"param-gearbox")]/b',
    "engine": './/span[contains(@class,"param-engine")]/b',
    "location": './/span[contains(@class,"param-location")]/b',
    "price": './/div[@class="item-price"]'

}

price_values = [150, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000,
                12500, 15000, 17500, 20000, 25000, 30000, 45000, 60000, 70000, 80000, 90000, 100000]

year_values = [1925, 1927, 1930, 1940, 1950, 1960, 1965, 1970, 1975, 1980, 1985, 1986, 1987, 1988, 1989, 1990, 1991,
               1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
               2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]


# Function that inputs text into text box
# Need the XPath of the input box and the value itself.
def enter_option(box_xpath, value):
    box = driver.find_element(By.XPATH, box_xpath)
    pinfo("Box found")
    box.click()
    psuccess("Box clicked")
    key_enter = WebDriverWait(driver, timeout=3).until(
        EC.presence_of_element_located((By.XPATH, f'{box_xpath}/div/div[@class="input-text"]/input[@type="text"]'))
    )
    pinfo("Found input box")
    pinfo("Sending keys")
    key_enter.send_keys(value)
    psuccess("Keys sent")
    opts = box.find_element(By.XPATH, './/div/div/div[@style="display: block;"]')
    opts.click()
    psuccess("Option has been selected")


# Selects the option from a dropdown list
# Inputs = XPath of the dropdown menu, the value list, and the input value
def select_dropdown(drop_xpath, value_list, value):
    value = take_closest(value_list, value)
    pinfo(f"value {value} was chosen")
    selection = Select(driver.find_element(By.XPATH, drop_xpath))
    selection.select_by_value(str(value))


# Chooses the closes of the list given the input value
def take_closest(lst, value):
    pos = bisect_left(lst, value)

    if pos == 0:
        return lst[0]
    if pos == len(lst):
        return list[-1]
    before = lst[pos - 1]
    after = lst[pos]
    if after - value < value - before:
        return after
    else:
        return before


def search_fill(make, model=None, price_from=None, price_to=None, year_from=None, year_to=None):
    enter_option(xpaths["make_box"], make)
    if model is not None:
        enter_option(xpaths["model_box"], model)
    if price_from is not None:
        select_dropdown(xpaths["price_from"], price_values, price_from)
    if price_to is not None:
        select_dropdown(xpaths["price_to"], price_values,price_to)
    if year_from is not None:
        select_dropdown(xpaths["year_from"], year_values, year_from)
    if year_to is not None:
        select_dropdown(xpaths["year_to"], year_values, year_to)
    try:
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpaths["but_submit"]))
    except ElementClickInterceptedException:
        perror("Error when clicking submit!")


def get_last_page():
    try:
        container = driver.find_element(By.XPATH, xpaths["paginator"])
        selections = container.find_elements(By.XPATH, './/a/div')
        page = selections[-2].text
    except NoSuchElementException:
        pinfo("Next button not found, setting page to 1")
        page = 1
    return int(page)


def scrape(make):
    arr = []
    # page = 1
    # lastpage = get_last_page()
    lastpage = 3
    for i in range(lastpage):
        pinfo(f"scraping page {i+1}")
        # find the listing container
        container = driver.find_element(By.XPATH, xpaths["list_container"])
        # get all elements that are listings
        lists = container.find_elements(By.XPATH, './/article[contains(@class,"list-item")]')
        # page += 1
        for ad in lists:
            list_name = ad.find_element(By.XPATH, './/div/div/h2[@class="item-title"]').text
            model = list_name.removeprefix(make).strip()
            link = ad.find_element(By.XPATH, relative_xpaths["link"]).get_attribute('href')
            fuel = ad.find_element(By.XPATH, relative_xpaths["fuel"]).text
            year = ad.find_element(By.XPATH, relative_xpaths["year"]).text
            try:
                mileage = ad.find_element(By.XPATH, relative_xpaths["mileage"]).text
            except NoSuchElementException:
                mileage = None
            gearbox = ad.find_element(By.XPATH, relative_xpaths["gearbox"]).text
            engine = ad.find_element(By.XPATH, relative_xpaths["engine"]).text
            location = ad.find_element(By.XPATH, relative_xpaths["location"]).text
            price = ad.find_element(By.XPATH, relative_xpaths["price"]).text
            arr.append(listing(make, model, link, year, fuel, location, mileage, gearbox))
        if i+1 != lastpage:
            # driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, xpaths["but_next"]))
            driver.find_element(By.XPATH, xpaths["but_next"]).click()
    return arr


def captcha_accept():
    pinfo("Looking for CAPTCHA")
    if EC.presence_of_element_located((By.XPATH, xpaths["captcha_accept"])):
        pinfo("CAPTCHA found")
        driver.find_element(By.XPATH, xpaths["captcha_accept"]).click()
        psuccess("CAPTCHA accepted")


def main(make, model=None, price_from=None, price_to=None, year_from=None, year_to=None):
    # obj_arr = []
    pinfo("Getting website")
    driver.get(website)
    psuccess("Website accessed")
    captcha_accept()
    pinfo("Filling search")
    search_fill(make, model, price_from, price_to, year_from, year_to)
    psuccess("Search successfully filled")
    pinfo("Starting to scrape pages")
    obj_arr = scrape(make)
    psuccess("Pages successfully scraped")
    pinfo("Driver is quitting")
    driver.quit()
    pinfo("Returning object array")
    return obj_arr
