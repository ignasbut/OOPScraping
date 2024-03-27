import undetected_chromedriver as uc

# TODO: Instead of generating custom URL, just use the search function via the website itself.
# This will make it easier to actually make the search queries
# As of now, only AUTOPLIUS can take in user-defined input, but AUTOGIDAS will need navigation via JS
# However, AUTOGIDAS has a more reasonable and text-based search for URL generation

class listing:
    def __init__(self, make, model, year, fuel_type, location, url, mileage=None, ) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.url = url
        self.location = location

    def update_attr(self, attr, val):
        setattr(self, attr, val)

class listing_extension(listing):
    def __init__(self, desc=None, color=None, defects=None, reserved=None):
        self.desc = desc
        self.color = color
        self.defects = defects
        self.reserved = reserved

    def update_attr(self, attr, val):
        setattr(self, attr, val)

