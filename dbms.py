import sqlite3


class CarDB:
    _instance = None

    def __new__(cls, database):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__database = database
            cls._instance.__conn = None
            cls._instance.__create_connection()
        return cls._instance

    def __create_connection(self):
        try:
            self.__conn = sqlite3.connect(self.__database)
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        if self.__conn:
            self.__conn.close()
            print("Database connection closed.")

    def create_table(self):
        try:
            sql_create_cars_table = """CREATE TABLE IF NOT EXISTS cars (
                                    id INTEGER PRIMARY KEY,
                                    make TEXT,
                                    model TEXT,
                                    year INTEGER,
                                    mileage INTEGER,
                                    trans TEXT,
                                    engine TEXT,
                                    fuel_type TEXT,
                                    driven_wheels TEXT,
                                    price TEXT,
                                    url TEXT UNIQUE,
                                    location TEXT
                                    );"""
            self.__execute_query(sql_create_cars_table)
            print("Table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_or_update_car(self, data):
        sql_check_existing = "SELECT * FROM cars WHERE url = ?"
        sql_update_data = ''' UPDATE cars
                              SET make = ?,
                                  model = ?,
                                  year = ?,
                                  mileage = ?,
                                  trans = ?,
                                  engine = ?,
                                  fuel_type = ?,
                                  driven_wheels = ?,
                                  price = ?,
                                  location = ?
                              WHERE url = ? '''
        sql_insert_data = ''' INSERT INTO cars(make, model, year, mileage, trans, engine, fuel_type, driven_wheels, price, url, location)
                              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = self.__conn.cursor()

        # Check if the URL already exists in the database
        cur.execute(sql_check_existing, (data["url"],))
        existing_car = cur.fetchone()

        if existing_car:
            # URL already exists, update the existing record
            cur.execute(sql_update_data, (
                data["make"],
                data["model"],
                data["year"],
                data["mileage"],
                data["trans"],
                data["engine"],
                data["fuel_type"],
                data["driven_wheels"],
                data["price"],
                data["url"],
                data["location"]
            ))
            print("Car data updated successfully!")
        else:
            # URL doesn't exist, insert new record
            cur.execute(sql_insert_data, (
                data["make"],
                data["model"],
                data["year"],
                data["mileage"],
                data["trans"],
                data["engine"],
                data["fuel_type"],
                data["driven_wheels"],
                data["price"],
                data["url"],
                data["location"]
            ))
            print("New car data inserted successfully!")

        self.__conn.commit()

    def get_car_data_from_array(self, arr):

        for obj in arr:
            data = {
                "make": obj[0],
                "model": obj[1],
                "year": obj[2],
                "mileage": obj[3],
                "trans": obj[4],
                "engine": obj[5],
                "fuel_type": obj[6],
                "driven_wheels": obj[7],
                "price": obj[8],
                "url": obj[9],
                "location": obj[10]
            }

            self.insert_or_update_car(data)
            # x = x + 8

    def __execute_query(self, query, data=None):
        try:
            if not self.__conn:
                self.__create_connection()
            cursor = self.__conn.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def extract_data(self):
        sql_select_all = "SELECT * FROM cars"
        cur = self.__conn.cursor()
        cur.execute(sql_select_all)
        rows = cur.fetchall()
        for row in rows:
            print(row)


# Usage example:
if __name__ == "__main__":
    db = CarDB("Car_DB.db")

    db.create_table()

    # db.extract_data()
    #
    # db.get_car_data_from_array()
    #
    db.close_connection()