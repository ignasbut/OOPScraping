class listing:
    def __init__(self, make=None, model=None, url=None, year=None, fuel_type=None, location=None, mileage=None, trans=None) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.url = url
        self.location = location
        self.trans = trans

    def update_attr(self, attr, val):
        setattr(self, attr, val)

    def print_info(self):
        print(f"Make: {self.make}\nModel: {self.model}\nYear: {self.year}\nFuel: {self.fuel_type}\n"
              f"Mileage: {self.mileage}\nLink: {self.url}\nLocation: {self.location}\nGearbox: {self.trans}")


class listing_extension(listing):
    def __init__(self, make=None, model=None, url=None, year=None, fuel_type=None, location=None, mileage=None,
                 desc=None, color=None, defects=None, reserved=None):
        super().__init__(make, model, url, year, fuel_type, location, mileage)
        self.desc = desc
        self.color = color
        self.defects = defects
        self.reserved = reserved

    @classmethod
    def from_listing(cls, listing_obj, desc=None, color=None, defects=None, reserved=None):
        return cls(listing_obj.make, listing_obj.model, listing_obj.year, listing_obj.fuel_type, listing_obj.mileage,
                   listing_obj.url, listing_obj.location, desc, color, defects, reserved)
