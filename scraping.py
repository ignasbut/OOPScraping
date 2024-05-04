# import autogidas
# import autoplius
# import brc
import threading
import importlib


def prts(objects):
    print(f"Number of scraped objects: {len(objects)}")

    for obj in objects:
        print("--------------------------")
        obj.print_info()


# def decorator(brand, model, price_from=None, price_to=None, year_from=None, year_to=None,):
def decorator(src, *args):
    arr = []
    threads = []
    for arg in src:
        arg = importlib.import_module(arg)
        threads.append(threading.Thread(target=arg.get_objects, args=[*args]))

    for thread in threads:
        print(f"Starting thread {thread.name}")
        thread.start()

    for thread in threads:
        print("thread disabled")
        thread.join()


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
    sources = ["autogidas", "autoplius", "brc"]
    decorator(sources, brand, model, None, None, year_from, year_to)
    # prts(arr) ; this is for printing

# start()


# conv_obj("BMW", "X5", None, None)

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
