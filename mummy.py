import math

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle




class Mummy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 0.9
        with self.canvas:
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source="src/momies/momia.png"  # ruta a tu imagen PNGangle
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def follow_player(self, player_x: float, player_y: float):


        if player_x >= self.x:
            x_triangle = self.x - player_x
            y_triangle = self.y - player_y
            if x_triangle == 0:
                x_triangle += 1

            angle = math.atan(y_triangle/x_triangle)
            self.x += math.cos(angle) * self.velocity
            self.y += math.sin(angle) * self.velocity
        else:
            x_triangle = self.x - player_x
            y_triangle = self.y - player_y
            if x_triangle == 0:
                x_triangle += 1
            angle = math.atan(y_triangle / x_triangle)
            self.x -= math.cos(angle) * self.velocity
            self.y -= math.sin(angle) * self.velocity

