from abc import ABC, abstractmethod
# class Car:
#     def __init__(self, brand, model, year_from, year_to, mileage, transmission, engine_volume, fuel_type, driven_wheels, price_from, price_to):
#         self.brand = brand
#         self.model = model
#         self.year_from = year_from
#         self.year_to = year_to
#         self.mileage = mileage
#         self.transmission = transmission
#         self.engine_volume = engine_volume
#         self.fuel_type = fuel_type
#         self.driven_wheels = driven_wheels
#         self.price_from = price_from
#         self.price_to = price_to
#
#     def __str__(self):
#         return f"{self.brand} {self.model} ({self.year}) {self.mileage} km {self.transmission} {self.engine_volume}L {self.fuel_type} {self.driven_wheels}"
#

# davaj padarom taip:
# we have abstract class called Car(ABC). Then, 2 subclasses: Listing and Query
# Query will have all the _from and _to attributes, which will be used for the search
# Listing will have the definitive values of the ad
# We can also add some sort of random function that follows the abstraction (idk like return_values or something)


class Car(ABC):
    def __init__(self, brand, model=None, transmission=None, engine_volume=None, fuel_type=None, driven_wheels=None):
        self.brand = brand
        self.model = model
        self.transmission = transmission
        self.engine_volume = engine_volume
        self.fuel_type = fuel_type
        self.driven_wheels = driven_wheels

    @abstractmethod
    def return_car(self):
        pass


class Query(Car):
    def __init__(self, brand, model, year_from, year_to, mileage_from, mileage_to, transmission, engine_volume,
                 fuel_type, driven_wheels, price_from, price_to):
        super().__init__(brand, model, transmission, engine_volume, fuel_type, driven_wheels)
        self. year_from = year_from
        self.year_to = year_to
        self.mileage_from = mileage_from
        self.mileage_to = mileage_to
        self.price_from = price_from
        self.price_to = price_to

    def return_car(self):
        return dir(self)

    def query_summary(self):
        return (f"{self.brand} {self.model} {self.year_from} - {self.year_to} {self.mileage_from} - {self.mileage_to}km"
                f"{self.transmission} {self.engine_volume}L {self.fuel_type} {self.driven_wheels} "
                f"{self.price_from} - {self.price_to} Eur")


class Listing(Car):
    def __init__(self, brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price, url,
                 location):
        super().__init__(brand, model, transmission, engine_volume, fuel_type, driven_wheels)
        self. year = year
        self.mileage = mileage
        self.price = price
        self.url = url
        self.location = location

    def return_car(self):
        return dir(self)


class ListingExtension(Listing):
    def __init__(self, brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price, url,
                 location, desc, color):
        super().__init__(brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price, url,
                         location)
        self.desc = desc
        self.color = color

    def print_desc(self):
        print(self.desc)

    @classmethod
    def from_listing(cls, listing_obj, desc=None, color=None):
        return cls(listing_obj.make, listing_obj.model, listing_obj.year, listing_obj.fuel_type, listing_obj.mileage,
                   listing_obj.url, listing_obj.location, desc, color)