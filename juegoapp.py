from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', True)

Config.set('kivy', 'pause_on_resume', 0)

from kivy.core.window import Window
Window.fullscreen = True      # Se verá fullscreen tanto en PC como en Android

from kivy.app import App
from screencontroler import ScreenController

class JuegoApp(App):
    def build(self):
        return ScreenController()
