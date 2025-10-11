from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class ScreenNewLevel(Screen):
    def __init__(self, level: int, **kwargs):
        super().__init__(**kwargs)
        self.label = ""
        Window.size = (800, 450)
        self.level = level

        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)



    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size

    def go_to_game(self, dt):
        game_screen = self.manager.get_screen("game")
        self.manager.current = "game"

    def set_level(self, new_level: int):
        self.level = new_level
        return str(self.level)

    def generate_screen(self):
        self.bind(size=self.update_bg, pos=self.update_bg)
        self.label = Label(text="Nivel..." + str(self.level), font_size=40, color=(1, 1, 1, 1))
        self.add_widget(self.label)
        Clock.schedule_once(self.go_to_game, 2)
