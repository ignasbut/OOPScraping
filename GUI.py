import time
import threading
import kivy
import asyncio
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.app import async_runTouchApp
import webbrowser
import scraping
from car import Query
import car
import dbms
import sys
import os

if sys.platform == 'darwin':  # macOS
    import pync
    from functools import partial
    from mac_notifications import client
# elif sys.platform == 'win32' or sys.platform == 'win64':  # Windows
    # from win10toast import ToastNotifier

from functools import partial

# import threading

Builder.load_file('noticar.kv')




class MyLayout(Widget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.brand = ""
        self.model = ""
        self.year_from = ""
        self.year_to = ""
        self.mileage_from = ""
        self.mileage_to = ""
        self.transmission = ""
        self.engine_vol = ""
        self.fuel = ""
        self.driven_wheels = ""
        self.price_from = ""
        self.price_to = ""

    car_values = []

    def brand_spinner_clicked(self, value):
        self.ids.brand_spinner.text = value

    def mileage_from_clicked(self, value):
        self.ids.mileage_from_spinner.text = value

    def mileage_to_clicked(self, value):
        self.ids.mileage_to_spinner.text = value

    def transmission_clicked(self, value):
        self.ids.transmission_spinner.text = value

    def fuel_clicked(self, value):
        self.ids.fuel_spinner.text = value

    def driven_wheels_clicked(self, value):
        self.ids.driven_wheels_spinner.text = value

    car_details = []
    query_list = []

    brand_input = ObjectProperty(None)
    model_input = ObjectProperty(None)
    year_from_input = ObjectProperty(None)
    year_to_input = ObjectProperty(None)
    mileage_from_input = ObjectProperty(None)
    mileage_to_input = ObjectProperty(None)
    transmission_input = ObjectProperty(None)
    engine_vol_input = ObjectProperty(None)
    driven_wheels_input = ObjectProperty(None)
    price_from_input = ObjectProperty(None)
    price_to_input = ObjectProperty(None)

    def clear_input_fields(self):
        self.ids.brand_spinner.text = ''
        self.ids.model_input.text = ''
        self.ids.year_from_input.text = ''
        self.ids.year_to_input.text = ''
        self.ids.mileage_from_spinner.text = ''
        self.ids.mileage_to_spinner.text = ''
        self.ids.transmission_spinner.text = ''
        self.ids.engine_vol_input.text = ''
        self.ids.fuel_spinner.text = ''
        self.ids.driven_wheels_spinner.text = ''
        self.ids.price_from_input.text = ''
        self.ids.price_to_input.text = ''

    def check_for_errors(self):
        invalid_chars = ",./;*+-[]<>:;'\§±{}_=_!@#$%^&*()ĄČĘĖĮŠŲŪŽąčęėįšųūž"
        error_found = False

        fields_to_check = [
            self.ids.model_input.text,
            self.ids.year_from_input.text,
            self.ids.year_to_input.text,
            self.ids.price_from_input.text,
            self.ids.price_to_input.text
        ]

        for field in fields_to_check:
            if any(char in field for char in invalid_chars):
                error_found = True
                break


        if any(char in self.ids.engine_vol_input.text for char in invalid_chars if char != "."):
            error_found = True

        return error_found


    def press(self):
        popup = Popup(title='Invalid input(s)',
                      content=Label(text="You used invalid characters. For engine volume use: ."),
                      size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 0.9},
                      )
        label = popup.content
        label.font_size = 24

        if self.check_for_errors():
            self.clear_input_fields()
            popup.open()
            return

        self.brand = self.ids.brand_spinner.text
        self.model = self.ids.model_input.text
        self.year_from = self.ids.year_from_input.text
        self.year_to = self.ids.year_to_input.text
        self.mileage_from = self.ids.mileage_from_spinner.text
        self.mileage_to = self.ids.mileage_to_spinner.text
        self.transmission = self.ids.transmission_spinner.text
        self.engine_vol = self.ids.engine_vol_input.text
        self.fuel = self.ids.fuel_spinner.text
        self.driven_wheels = self.ids.driven_wheels_spinner.text
        self.price_from = self.ids.price_from_input.text
        self.price_to = self.ids.price_to_input.text

        query = Query(self.brand, self.model, self.year_from, self.year_to, self.mileage_from, self.mileage_to, self.transmission,
                      self.engine_vol, self.fuel, self.driven_wheels, self.price_from, self.price_to)

        search_summary = Label(text=query.query_summary())

        self.query_list.append(query)

        self.ids.selected_car.clear_widgets()

        for q in self.query_list:
            self.ids.selected_car.add_widget(Label(text=q.query_summary()))

        self.canvas.ask_update()

        print(
            f' {self.brand} {self.model} {self.year_from} {self.year_to} {self.mileage_from}, mileage to: {self.mileage_to} {self.transmission} {self.engine_vol} {self.fuel} {self.driven_wheels} {self.price_from} {self.price_to}')

        self.clear_input_fields()

        scraping.conv_obj(self.brand, self.model, self.year_from, self.year_to, self.mileage_from, self.mileage_to, self.transmission,
                      self.engine_vol, self.fuel, self.driven_wheels, self.price_from, self.price_to)

        self.app.show_notification(self)

    def update(self):

        # scraping.conv_obj(self.brand, self.model, self.year_from, self.year_to, self.mileage_from, self.mileage_to, self.transmission,
        #               self.engine_vol, self.fuel, self.driven_wheels, self.price_from, self.price_to)

        self.app.show_notification(self)
        db = dbms.CarDB("Car_DB.db")
        self.ids.new_listings.clear_widgets()

        records = db.extract_data()

        for record in records:
            car_info = ''
            arr = list(record.values())
            code=arr[-2]
            del arr[-2]

            for val in arr:
                car_info += str(val) + " "

            link_button = Button(text=car_info,
                                 size_hint_y= None,
                                 height=50
                                 )
            link_button.bind(on_press=partial(self.open_link, code))

            #link_button.bind(on_press=partial(self.open_link, code))

            self.ids.new_listings.add_widget(link_button)
            self.canvas.ask_update()


        self.ids.scroll_view.do_scroll_y = True
        self.canvas.ask_update()



    def open_link(self, url, instance):
        webbrowser.open(url)







class NotiCarApp(App):
    def build(self):
        #Window.clearcolor = (28 / 255.0, 99 / 255.0, 158 / 255.0, 0.75)
        return MyLayout(self)

    def show_notification(self, instance):
        title = "New listing(s)"
        message = "There are some updates for your request(s)."


        script_path = os.path.abspath('show_notification_with_icon.applescript')
        icon_path = os.path.abspath('added-64.png')

        script = f'{script_path} {icon_path} "{title}" "{message}"'

        if sys.platform == 'win32' or sys.platform == 'win64':  # Windows
            toaster = ToastNotifier()
            toaster.show_toast(title, message)

        elif sys.platform == 'darwin':
            client.create_notification(
            title,
            subtitle=message,
            icon=icon_path

        )

if __name__ == '__main__':
    NotiCarApp().run()

# Async

#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     NotiCarApp().async_run())
# loop.close()

# Threading
# t1 = threading.Thread(target=NotiCarApp().run())
#
# t1.start()
# time.sleep(4)
# t1.join()