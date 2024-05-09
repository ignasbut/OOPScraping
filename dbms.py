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
            self.__conn = sqlite3.connect(self.__database, check_same_thread=False)
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        if self.__conn:
            self.__conn.close()
            print("Database connection closed.")

    def create_table1(self):
        try:
            sql_create_cars_table = """CREATE TABLE IF NOT EXISTS cars1 (
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

    def create_table2(self):
        try:
            sql_create_cars_table = """CREATE TABLE IF NOT EXISTS cars2 (
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

    def insert_car(self, data):
        
        sql_insert_data_cars2 = ''' INSERT INTO cars2(make, model, year, mileage, trans, engine, fuel_type, driven_wheels, price, url, location)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        
        cur = self.__conn.cursor()

    # Insert data into cars2
        cur.execute(sql_insert_data_cars2, (
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
        print("New car data inserted successfully into cars2!")
 
   
        self.__conn.commit()
        # self.close_connection()
    
    def delete_old_cars(self):
        sql_delete_old_cars = """ DELETE FROM cars2 WHERE url IN (SELECT url FROM cars2 INTERSECT SELECT url FROM cars1) """
        cur = self.__conn.cursor()
        cur.execute(sql_delete_old_cars)
        print("Old cars deleted successfully from cars2!")
        self.__conn.commit()
        # self.close_connection()

    def insert_new_cars_to_cars1(self):
        sql_insert_new_cars = """ INSERT INTO cars1 (make, model, year, mileage, trans, engine, fuel_type, driven_wheels, price, url, location) 
            SELECT make, model, year, mileage, trans, engine, fuel_type, driven_wheels, price, url, location
            FROM cars2
            WHERE url NOT IN (SELECT url FROM cars1) """
        cur = self.__conn.cursor()
        cur.execute(sql_insert_new_cars)
        print("New cars inserted into cars1!")
        self.__conn.commit()
        # self.close_connection()
        
    
        
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

            # Insert data into cars2
            self.insert_car(data)

        

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
        sql_select_all = "SELECT * FROM cars2"
        cur = self.__conn.cursor()
        cur.execute(sql_select_all)
        rows = cur.fetchall()
        obj_arr = []  
    
        for obj in rows:
            inst = {
                "id": obj[0],
               "make": obj[1],
                "model": obj[2],
                "year": obj[3],
                "mileage": obj[4],
                "trans": obj[5],
                "engine": obj[6],
                "fuel_type": obj[7],
                "driven_wheels": obj[8],
                "price": obj[9],
                "url": obj[10],
                "location": obj[11]
                }
            obj_arr.append(inst)
        return obj_arr
    
    

# Usage example:
if __name__ == "__main__":
    db = CarDB("Car_DB.db")

    db.create_table1()
    db.create_table2()
    db.get_car_data_from_array()

    db.insert_new_cars_to_cars1()
    db.delete_old_cars()
    
    
    db.extract_data()

    db.close_connection()

