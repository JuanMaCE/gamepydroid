from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle




class Mummy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(255, 1, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

