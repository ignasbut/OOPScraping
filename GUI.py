from kivy.app import App
from kivy.uix.label import Label

class myApp(App):
    def build(self):
        label=Label(text="Let's go!")
        return label

app=myApp()
app.run()