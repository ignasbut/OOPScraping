import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

Builder.load_file('noticar.kv')
class MyLayout(Widget):



    def brand_spinner_clicked(self, value):
        self.ids.brand_spinner.text=value

    def mileage_from_clicked(self, value):
        self.ids.mileage_from_spinner.text=value

    def mileage_to_clicked(self, value):
        self.ids.mileage_to_spinner.text=value

    def transmission_clicked(self, value):
        self.ids.transmission_spinner.text=value

    def fuel_clicked(self, value):
        self.ids.fuel_spinner.text=value

    def driven_wheels_clicked(self, value):
        self.ids.driven_wheels_spinner.text=value



    brand_input=ObjectProperty(None)
    model_input = ObjectProperty(None)
    year_from_input = ObjectProperty(None)
    year_to_input = ObjectProperty(None)
    mileage_from_input=ObjectProperty(None)
    mileage_to_input=ObjectProperty(None)
    transmission_input=ObjectProperty(None)
    engine_vol_input=ObjectProperty(None)
    driven_wheels_input=ObjectProperty(None)
    price_from_input=ObjectProperty(None)
    price_to_input=ObjectProperty(None)

    def press(self):
        brand=self.ids.brand_spinner.text
        model=self.model_input.text
        year_from =self.year_from_input.text
        year_to=self.year_to_input.text
        mileage_from=self.ids.mileage_from_spinner.text
        mileage_to = self.ids.mileage_to_spinner.text
        transmission=self.ids.transmission_spinner.text
        engine_vol=self.engine_vol_input.text
        fuel=self.ids.fuel_spinner.text
        driven_wheels=self.ids.driven_wheels_spinner.text
        price_from = self.price_from_input.text
        price_to = self.price_to_input.text




        # Create a Label with search criteria
        search_summary = Label(text=f"{brand} {model} {year_from} - {year_to} {mileage_from} - {mileage_to}km {transmission} {engine_vol}L {fuel} {driven_wheels} {price_from} - {price_to} Eur")

        # Add the Label to the layout (assuming 'your_layout_id' is the parent)
        self.ids.selected_car.add_widget(search_summary)

        self.canvas.ask_update()


        print(f'Brand: {brand}, model: {model}, year from: {year_from}, year to: {year_to}, mileage from: {mileage_from}, mileage to: {mileage_to}, transmission: {transmission}, engine volume: {engine_vol}, fuel type: {fuel}, driven wheels: {driven_wheels}, price from: {price_from}, price to: {price_to}')

        self.ids.brand_spinner.text=''
        self.model_input.text =''
        self.year_from_input.text =''
        self.year_to_input.text = ''
        self.ids.mileage_from_spinner.text=''
        self.ids.mileage_to_spinner.text=''
        self.ids.transmission_spinner.text=''
        self.engine_vol_input.text=''
        self.ids.fuel_spinner.text=''
        self.ids.driven_wheels_spinner.text=''
        self.price_from_input.text=''
        self.price_to_input.text=''



class NotiCarApp(App):
    def build(self):
        Window.clearcolor=(28/255.0, 99/255.0, 158/255.0, 0.75)
        return MyLayout()

NotiCarApp().run()