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
                                    fuel_type TEXT,
                                    mileage INTEGER,
                                    url TEXT UNIQUE,
                                    location TEXT,
                                    trans TEXT
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
                                  fuel_type = ?,
                                  mileage = ?,
                                  location = ?,
                                  trans = ?
                              WHERE url = ? '''
        sql_insert_data = ''' INSERT INTO cars(make, model, year, fuel_type, mileage, url, location, trans)
                              VALUES(?,?,?,?,?,?,?,?) '''
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
                data["fuel_type"],
                data["mileage"],
                data["location"],
                data["trans"],
                data["url"]
            ))
            print("Car data updated successfully!")
        else:
            # URL doesn't exist, insert new record
            cur.execute(sql_insert_data, (
                data["make"],
                data["model"],
                data["year"],
                data["fuel_type"],
                data["mileage"],
                data["url"],
                data["location"],
                data["trans"]
            ))
            print("New car data inserted successfully!")

        self.__conn.commit()    

    def get_car_data_from_array(self):
        from scraped_objects import conv_obj
       
        car_data_array = conv_obj()
        i = len(car_data_array) 
        x = 0

        while x < i:
            make = car_data_array[x+0]  
            model = car_data_array[x+1] 
            year = car_data_array[x+2]
            fuel_type = car_data_array[x+3]
            mileage = car_data_array[x+4]
            url = car_data_array[x+5]
            location = car_data_array[x+6]
            trans = car_data_array[x+7]
            
        
            data = {
                "make": make,
                "model": model,
                "year": year,
                "fuel_type": fuel_type,
                "mileage": mileage, 
                "url": url,
                "location": location,
                "trans": trans,
            }
        
            self.insert_or_update_car(data)
            x = x + 8

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

    db.extract_data()

    db.get_car_data_from_array()

    db.close_connection()
