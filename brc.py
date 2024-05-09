import os
import time
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from bisect import bisect_left
from car import Listing, ListingExtension
import dbms

website = "https://lt.brcauto.eu/en/cars-search"
root = "https://lt.brcauto.eu/"

def pinfo(*args):
    print("[*] ", *args)


def perror(*args):
    print("[!] ", *args)


def psuccess(*args):
    print("[+] ", *args)

xpaths = {
    "make": '//label[@class="block py-2"][1]/div[@class="multiselect"]',
    "make_opt": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[1]/label[1]/div/div[3]/ul/li[1]/span/div',
    "model": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[1]/label[2]/div',
    "model_opt": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[1]/label[2]/div/div[3]/ul/li[1]/span',
    "price_from": '//input[@name="price_from"]',
    "price_to": '//input[@name="price_to"]',
    "year_from": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div',
    "year_from_opt": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[3]/ul/li[1]/span',
    "year_to": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div',
    "year_to_opt": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div[3]/ul/li[1]/span',
    "mileage_from": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/label[1]/input',
    "mileage_to": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/label[2]/input',
    "fuel_type": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[1]/div[2]/label/div/div',
    "fuel_type_opt": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[1]/div[2]/label/div/div/div[3]/ul/li[1]/span',
    "detailed_search": '//a[@id="display-detailed-filter"]',
    "gearbox": '',
    "submit": '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[3]/div/button',
    "listing_container": '//div[contains(@class, "cars-container")]',
    "paginator": '//nav[@class="pagination"]/ul[@class="pagination"]',
}

relative_xpaths = {
    "listing": './/div[@class="cars-wrapper"]/div[@class="cars"]',
    "title_url": './/div[@class="cars__top"]/h2/a',
    "info": './/div[@class="cars__top"]/p[@class="cars__subtitle"]',
    "price": './/div[@class="cars__middle"]/div/div[contains(@class, "cars-price")]',
    "location": './/div[@class="cars__bottom"]/div/span/img',
}

global driver

def select_gearbox(value):
    if value.lower() == "manual":
        driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div[1]').click()
    elif value.lower() == "automatic":
        driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div[2]').click()
    else:
        driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[1]/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div[3]').click()

def enter_option(box_xpath, opt_xpath, value):
    box = driver.find_element(By.XPATH, box_xpath)
    pinfo("Box found")
    box.click()
    psuccess("Box clicked")
    box.find_element(By.XPATH, './/div/input[@class="multiselect__input"]').send_keys(value)
    pt = f'{box_xpath}/div/ul/li[1]/span/div'
    opt = WebDriverWait(driver, timeout=3).until(
        ec.element_to_be_clickable((By.XPATH, opt_xpath))
    )
    opt.click()
    psuccess("Option clicked")
    driver.send_keys("html", Keys.ESCAPE)


def enter_year(box_xpath, value):
    box = driver.find_element(By.XPATH, box_xpath)
    pinfo("Box found")
    box.click()
    psuccess("Box clicked")
    box.send_keys(value)


def type_option(box_xpath, value):
    box = driver.find_element(By.XPATH, box_xpath)
    pinfo("Box found")
    box.click()
    box.send_keys(value)

def get_pages():
    try:
        page = driver.find_element(By.XPATH, xpaths["paginator"])
        num = page.find_elements(By.XPATH, './li[@class="page-item"]')[-2].text
    except NoSuchElementException:
        num = 1
    return int(num)


def search_fill(make, model=None, price_from=None, price_to=None, year_from=None, year_to=None, mileage_from=None,
                mileage_to=None, driven_wheels=None):
    driver.find_element(By.XPATH, xpaths["detailed_search"]).click()
    enter_option(xpaths["make"], xpaths["make_opt"], make)
    if model is not None:
        enter_option(xpaths["model"], xpaths["model_opt"], model)
    if price_from is not None:
        type_option(xpaths["price_from"], price_from)
    if price_to is not None:
        type_option(xpaths["price_to"], price_to)
    if year_from is not None:
        enter_option(xpaths["year_from"], xpaths["year_from_opt"], year_from)
    if year_to is not None:
        enter_option(xpaths["year_to"], xpaths["year_to_opt"] , year_to)
    if mileage_from is not None:
        type_option(xpaths["mileage_from"], mileage_from)
    if mileage_to is not None:
        type_option(xpaths["mileage_to"], mileage_to)

    # driver.find_element(By.XPATH, xpaths["submit"]).click()
    driver.uc_click(xpaths["submit"], by="xpath")

def scraping(make, driven_wheels):
    arr = []
    pages = get_pages()
    print(pages)

    for i in range(pages):
        container = driver.find_element(By.XPATH, xpaths["listing_container"])
        listings = container.find_elements(By.XPATH, relative_xpaths["listing"])

        for listing in listings:
            info = listing.find_element(By.XPATH, relative_xpaths["info"]).text.split(" | ")
            model = listing.find_element(By.XPATH, relative_xpaths["title_url"]).text.removeprefix(make).strip()
            url = listing.find_element(By.XPATH, relative_xpaths["title_url"]).get_attribute("href")
            if "Hybrid" in info[0] or "Electric" in info[0]:
                fuel_type = info[0].split("-")[0]
                engine_vol = info[0].split("-")[-1]
                gearbox = info[1]
                horsepower = info[2]
                mileage = info[3]
                year = "N/A"
            else:
                year = info[0]
                engine_vol = info[1].split(" ")[0]
                fuel_type = info[1].split(" ")[1]
                gearbox = info[2]
                mileage = info[3]
                horsepower = info[4]
            # price = listing.find_element(By.XPATH, relative_xpaths["price"]).text.strip()
            try:
                price = driver.execute_script("""
            return jQuery(arguments[0]).contents().filter(function() {
                return this.nodeType == Node.TEXT_NODE;
            }).text();
            """, listing.find_element(By.XPATH, relative_xpaths["price"])).strip()
            except NoSuchElementException:
                price = "N/A"
            if gearbox == "Automatic":
                try:
                    model = model.removesuffix(" Automatas")
                    model = model. removesuffix(" A/T")
                except ValueError:
                    continue
            location = listing.find_element(By.XPATH, relative_xpaths["location"]).get_attribute("alt").removeprefix("BRC ")
            if driven_wheels is None:
                driven_wheels = "N/A"
            arr.append(Listing(make, model, year, mileage, gearbox, engine_vol, fuel_type, driven_wheels, price,
                                   url, location))

        if i+1 != pages:
            driver.find_elements(By.XPATH, f'{xpaths["paginator"]}/li')[-1].find_element(By.XPATH, './/a').click()
    return arr


def get_objects(make, model=None, price_from=None, price_to=None, year_from=None, year_to=None, mileage_from=None,
                mileage_to=None, driven_wheels=None):
    try:
        global driver
        driver = Driver(uc=True, ad_block_on=True, headless=False)
        driver.maximize_window()
        obj_arr = []
        pinfo("Getting website")
        driver.get(website)
        psuccess("Website accessed")
        pinfo("Filling search")
        try:
            driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/a[1]').click()
        except:
            driver.save_screenshot("error.png")
        search_fill(make, model, price_from, price_to, year_from, year_to, mileage_from, mileage_to, driven_wheels)
        psuccess("Search successfully filled")
        pinfo("Starting to scrape pages")
        for obj in scraping(make, driven_wheels):
            obj_arr.append(obj.return_car())
        # driver.close()
        db = dbms.CarDB("Car_DB.db")
        db.get_car_data_from_array(obj_arr)
        db.delete_old_cars()
        db.insert_new_cars_to_cars1()
        db.close_connection()
    finally:
        driver.quit()
        os.system("killall chrome")


# get_objects("BMW", None, None, None, None, None, None,
#            None, None)