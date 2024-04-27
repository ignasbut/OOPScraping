import time
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bisect import bisect_left
from listing_class import listing, listing_extension

driver = uc.Chrome(headless=False)
website = 'https://autogidas.lt/en/'

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
    "but_submit": '//button[@type="submit"]',
    "paginator": '//div[@class="paginator"]',
    "but_next": '//a[contains(div, "Next")]/div',
    "list_container": './/main/article',
}

# Remember that the index is +1 since there initially was a space at the start!
price_values = [150, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000,
                12500, 15000, 17500, 20000, 25000, 30000, 45000, 60000, 70000, 80000, 90000, 100000]

year_values = [1925, 1927, 1930, 1940, 1950, 1960, 1965, 1970, 1975, 1980, 1985, 1986, 1987, 1988, 1989, 1990, 1991,
               1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
               2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]


def enter_option(box_xpath, value):
    box = driver.find_element(By.XPATH,box_xpath)
    box.click()
    print("clicked box")
    key_enter = WebDriverWait(driver, timeout=3).until(
        EC.presence_of_element_located((By.XPATH, f'{box_xpath}/div/div[@class="input-text"]/input[@type="text"]'))
    )
    print("Found input box")
    key_enter.send_keys(value)
    print("sent keys")
    opts = box.find_element(By.XPATH, './/div/div/div[@style="display: block;"]')
    opts.click()


def select_dropdown(drop_xpath, value_list, value):
    value = take_closest(value_list, value)
    print(f"value {value} was chosen")
    selection = Select(driver.find_element(By.XPATH, drop_xpath))
    selection.select_by_value(str(value))


def take_closest(list, value):
    pos = bisect_left(list, value)

    if pos == 0:
        return list[0]
    if pos == len(list):
        return list[-1]
    before = list[pos - 1]
    after = list[pos]
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

    driver.find_element(By.XPATH, xpaths["but_submit"]).submit()


def get_last_page():
    try:
        container = driver.find_element(By.XPATH, xpaths["paginator"])
        selections = container.find_elements(By.XPATH, './/a/div')
        page = selections[-2].text
    except NoSuchElementException:
        page = 1
    return int(page)


def scrape(arr,make):
    # page = 1
    lastpage = get_last_page()

    for i in range(lastpage):
        print(f"scraping page {i+1}")
        # find the listing container
        container = driver.find_element(By.XPATH, xpaths["list_container"])
        # get all elements that are listings
        lists = container.find_elements(By.XPATH, './/article[contains(@class,"list-item")]')
        # page += 1
        for ad in lists:
            list_name = ad.find_element(By.XPATH,'.//div/div/h2[@class="item-title"]').text
            arr.append(listing(make, list_name.removeprefix(make).strip()))
        if i+1 != lastpage:
            driver.find_element(By.XPATH, xpaths["but_next"]).click()


def main(make, model=None, price_from=None, price_to=None, year_from=None, year_to=None):
    obj_arr = []
    driver.get(website)
    search_fill(make, model, price_from, price_to, year_from, year_to)
    scrape(obj_arr, make)
    time.sleep(4)
    driver.quit()
    return obj_arr
