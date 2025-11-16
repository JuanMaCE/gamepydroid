from kivy.config import Config

# 🔥 Estas dos líneas solucionan el problema de que Android arranque "chiquito"
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', True)

# Opcional pero recomendado para evitar comportamiento raro al reabrir
Config.set('kivy', 'pause_on_resume', 0)

# -- Después ya puedes importar Kivy --
from kivy.core.window import Window
Window.fullscreen = True      # Se verá fullscreen tanto en PC como en Android

from kivy.app import App
from screencontroler import ScreenController

class JuegoApp(App):
    def build(self):
        return ScreenController()
