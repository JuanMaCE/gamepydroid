import math
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


class Mummy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 0.9

        self.size = (40, 40)

        self.image_size = (80, 80)
        self.image_offset = (-20, -20)

        with self.canvas:
            self.rect = Rectangle(
                pos=(self.x + self.image_offset[0], self.y + self.image_offset[1]),
                size=self.image_size,
                source="src/momies/momia.png"
            )

        self.bind(pos=self.update_rect)

    def update_rect(self, *args):

        self.rect.pos = (self.x + self.image_offset[0], self.y + self.image_offset[1])

    def follow_player(self, player_x: float, player_y: float):
        x_diff = player_x - self.x
        y_diff = player_y - self.y
        angle = math.atan2(y_diff, x_diff)
        self.x += math.cos(angle) * self.velocity
        self.y += math.sin(angle) * self.velocity

    def set_new_velocity(self, new_ve: float):
        self.velocity += new_ve
