import sqlite3

class CarDB:
    def __init__(self, database):
        self.database = database
        self.conn = None
        self.create_connection()  # Create the connection in the constructor

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.database)
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
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
            self.execute_query(sql_create_cars_table)
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
        cur = self.conn.cursor()

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

        self.conn.commit()

    def execute_query(self, query, data=None):
        if not self.conn:
            self.create_connection()
        cursor = self.conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor
    

    def get_car_data_from_array(self):
        from scraping import conv_obj
       
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

    def execute_query(self, query, data=None):
        try:
            if not self.conn:
                self.create_connection()
            cursor = self.conn.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

# Usage example:
if __name__ == "__main__":
    db = CarDB("Car_DB.db")

    db.create_table()

    db.get_car_data_from_array()
    
    db.close_connection()
