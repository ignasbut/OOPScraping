import os, sys
import platform
import json
import datetime
import scraping
import prettyprint
import storage


def checkFirstRun():
        if os.path.isfile("./options.json"):
            with open("./options.json", "r") as options_file:
               data = json.load(options_file)
               data["last_run"] = f"{datetime.datetime.now()}"
            with open("./options.json", "w") as options_file:
                json.dump(data, options_file)
            options_file.close()
        else:
            with open("./options.json", "x") as options_file:
                data = {
                    "first_run": True,
                    "last_run": f"{datetime.datetime.now()}",
                    "os_platform": f"{platform.system()}"
                }

                options_file.write(json.dumps(data, indent=4))
            options_file.close()


if __name__ == '__main__':
    if checkFirstRun():
        print("Application has already run! Can proceed to loading saved data")
    else:
        print("First time running application! Generating options.json file")

    if input("Test?: ") == "y":
        test_obj = scraping.listing("Audi", "200", 1998, "Diesel", "Vilnius", "random.com")