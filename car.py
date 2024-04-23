class Car:
    def __init__(self, brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price_from, price_to):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage
        self.transmission = transmission
        self.engine_volume = engine_volume
        self.fuel_type = fuel_type
        self.driven_wheels = driven_wheels
        self.price_from = price_from
        self.price_to = price_to

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) {self.mileage} km {self.transmission} {self.engine_volume}L {self.fuel_type} {self.driven_wheels}"