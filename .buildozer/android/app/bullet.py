from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Rotate
import math
from kivy.core.window import Window

class Bullet(Widget):
    def __init__(self, angle=0, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 10  # píxeles por frame
        self.first_angle = True
        with self.canvas:
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source="src/bullet.png"  # ruta a tu imagen PNG
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.rotation = Rotate(origin=(Window.width / 2, Window.height / 2))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self, angle):
        self.rotation.angle += 1  # aumenta el ángulo cada frame
        if not self.first_angle:
            self.x += math.cos(self.angle) * self.velocity
            self.y += math.sin(self.angle) * self.velocity

        elif self.first_angle:
            self.angle = angle
            self.x += math.cos(angle) * self.velocity
            self.y += math.sin(angle) * self.velocity
            self.first_angle = False

