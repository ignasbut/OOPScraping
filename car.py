class Car:
    def __init__(self, brand, model, year_from, year_to, mileage, transmission, engine_volume, fuel_type, driven_wheels, price_from, price_to):
        self.brand = brand
        self.model = model
        self.year_from = year_from
        self.year_to = year_to
        self.mileage = mileage
        self.transmission = transmission
        self.engine_volume = engine_volume
        self.fuel_type = fuel_type
        self.driven_wheels = driven_wheels
        self.price_from = price_from
        self.price_to = price_to

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) {self.mileage} km {self.transmission} {self.engine_volume}L {self.fuel_type} {self.driven_wheels}"