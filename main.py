import os, sys
import platform
import json
import datetime
import scraping
from scraping import get_objects
import prettyprint
import storage
import asyncio
from GUI import NotiCarApp, MyLayout


def check_first_run():
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
    if check_first_run():
        print("Application has already run! Can proceed to loading saved data")
    else:
        print("First time running application! Generating options.json file")


    print(MyLayout.brand_input)