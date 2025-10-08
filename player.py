from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window




class Player(Widget):
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 1, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self):
        self.y += self.velocity_y
        self.x += self.velocity_x

        if self.y < 0:
            self.y = 0
        elif self.top > Window.height:
            self.top = Window.height

        if self.x < 0:
            self.x = 0
        elif self.top > Window.height:
            self.top = Window.height