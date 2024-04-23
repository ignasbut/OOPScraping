from car import Car
#from database import load_cars_from_db, add_car_to_db

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.properties import ObjectProperty


# import sqlite3

conn = sqlite3.connect('cars.db')  # Replace 'cars.db' with your desired database name
c = conn.cursor()

# Create table if it doesn't exist (Modify columns as needed)
c.execute('''CREATE TABLE IF NOT EXISTS cars (
                brand TEXT,
                model TEXT,
                year INTEGER,
                mileage INTEGER,
                transmission TEXT,
                engine_volume REAL,
                fuel_type TEXT,
                driven_wheels TEXT
            )''')

class NotiCar(App):
    car_list = ObjectProperty([])

    def __init__(self, **kwargs):
        super(NotiCar, self).__init__(**kwargs)
        self.car_list = self.load_cars_from_db()

    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        # Top row for input fields
        top_row = BoxLayout(orientation='horizontal')
        brand_input = TextInput(hint_text="Brand")
        model_input = TextInput(hint_text="Model")
        year_input = TextInput(hint_text="Year", input_filter='numeric')
        mileage_input = TextInput(hint_text="Mileage (km)", input_filter='numeric')
        transmission_input = TextInput(hint_text="Transmission")
        engine_volume_input = TextInput(hint_text="Engine Volume (L)", input_filter='numeric')
        fuel_type_input = TextInput(hint_text="Fuel Type")
        driven_wheels_input = TextInput(hint_text="Driven Wheels")
        top_row.add_widget(brand_input)
        top_row.add_widget(model_input)
        top_row.add_widget(year_input)
        top_row.add_widget(mileage_input)
        top_row.add_widget(transmission_input)
        top_row.add_widget(engine_volume_input)
        top_row.add_widget(fuel_type_input)
        top_row.add_widget(driven_wheels_input)


        add_button = Button(text="Add request", on_press=self.add_car)
        top_row.add_widget(add_button)


        car_list_view = ListView(item_strings=self.get_car_strings())  # Initial car list
        car_list_view.bind(on_selection_change=self.on_car_selection)  # Bind selection change event

        main_layout.add_widget(top_row)


if __name__ == "__main__":
    NotiCar().run()