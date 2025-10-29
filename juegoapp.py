from kivy.app import App
from screencontroler import ScreenController

class JuegoApp(App):
    def build(self):
        return ScreenController()
