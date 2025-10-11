from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random


# ======= SCREEN DE NUEVO NIVEL =======
class ScreenNewLevel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 450)
        self.level = 1

        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(text="Nivel..." + str(self.level),
                           font_size=40, color=(1, 1, 1, 1))
        self.add_widget(self.label)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size

    def set_level(self, new_level: int):
        self.level = new_level
        self.label.text = f"Nivel... {self.level}"
        # esperar 2 segundos y luego pasar al juego
        Clock.schedule_once(self.go_to_game, 2)

    def go_to_game(self, dt):
        game_screen = self.manager.get_screen("game")
        game_screen.load_level(self.level)
        self.manager.current = "game"


# ======= SCREEN DEL JUEGO =======
class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 450)
        with self.canvas:
            Color(0.1, 0.2, 0.3, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(text="Juego", font_size=40, color=(1, 1, 1, 1))
        self.add_widget(self.label)

        self.level = 1
        self.enemies = []

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size

    def load_level(self, level):
        """Carga o reinicia el nivel"""
        self.level = level
        self.label.text = f"Jugando nivel {self.level}"
        print(f"🟢 Iniciando nivel {self.level}")
        # simular ganar el nivel después de 4 segundos
        Clock.schedule_once(self.win_level, 4)

    def win_level(self, dt):
        print(f"🏁 Nivel {self.level} completado")
        next_level = self.level + 1
        # si quieres limitar niveles
        if next_level > 5:
            self.manager.current = "finish"
            return
        screen_new_level = self.manager.get_screen("screenNewLevel")
        screen_new_level.set_level(next_level)
        self.manager.current = "screenNewLevel"


# ======= SCREEN FINAL =======
class Finish(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(text="🎉 Has ganado el juego 🎉",
                           font_size=40, color=(1, 1, 1, 1))
        self.add_widget(self.label)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size


# ======= APP PRINCIPAL =======
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ScreenNewLevel(name="screenNewLevel"))
        sm.add_widget(Game(name="game"))
        sm.add_widget(Finish(name="finish"))

        # comenzar con el nivel 1
        sm.get_screen("screenNewLevel").set_level(1)
        sm.current = "screenNewLevel"
        return sm


MyApp().run()
