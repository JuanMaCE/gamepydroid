from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class Finish(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 450)

        with self.canvas:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)

        self.bind(size=self.update_bg, pos=self.update_bg)
        self.label = Label(text="MORISTE!!!", font_size=40, color=(1, 1, 1, 1))
        self.add_widget(self.label)



    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size

    def go_to_game(self, dt):
        self.manager.current = 'game'

