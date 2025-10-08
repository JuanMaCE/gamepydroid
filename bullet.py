from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import math

class Bullet(Widget):
    def __init__(self, angle=0, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 10  # píxeles por frame
        self.first_angle = True
        with self.canvas:
            Color(0, 1, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self, angle):
        # Mueve la bala en línea recta según su ángulo
        if not self.first_angle:
            self.x += math.cos(self.angle) * self.velocity
            self.y += math.sin(self.angle) * self.velocity

        elif self.first_angle:
            self.angle = angle
            self.x += math.cos(angle) * self.velocity
            self.y += math.sin(angle) * self.velocity
            self.first_angle = False

