from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Assuming your scraped car objects are stored in a list called 'cars'
# If they are retrieved from a different source, modify accordingly
from scraped_objects import cars  # Import your scraped car objects

Base = declarative_base()

class CarDB(Base):
    __tablename__ = 'cars'  # Name of the table in the database

    id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Integer)
    transmission = Column(String)
    engine_volume = Column(Float)
    fuel_type = Column(String)
    driven_wheels = Column(String)
    price = Column(Float)  # Changed to a single 'price' column

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) {self.mileage} km {self.transmission} {self.engine_volume}L {self.fuel_type} {self.driven_wheels} (price: {self.price})"

# Replace 'cars.db' with your desired database name
engine = create_engine('sqlite:///cars.db')  # Create the engine and database

# **Check 1: Table Creation**
print("Creating tables...")
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")  # Print any errors encountered

Session = sessionmaker(bind=engine)
session = Session()

# **Check 2: Empty Car List**
if not cars:
    print("Warning: 'cars' list is empty. No data to insert into database.")

for car in cars:
    # Assuming your scraped car objects have a 'price' attribute
    new_car_db = CarDB(price=car.price, **{k: v for k, v in car.__dict__.items() if k != 'price'})

    # **Check 3: CarDB Object Creation**
    # You can uncomment this to see each CarDB object created
    # print(f"Created CarDB object: {new_car_db}")

    # Add the CarDB instance to the session
    session.add(new_car_db)

# **Check 4: Commit Changes**
try:
    session.commit()
    print("Database population complete!")
except Exception as e:
    print(f"Error committing changes to database: {e}")  # Print any errors
    # Consider rolling back the session if there's an error (session.rollback())

session.close()
