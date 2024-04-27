class listing:
    def __init__(self, make, model, url=None, year=None, fuel_type=None, location=None, mileage=None, ) -> None:
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

