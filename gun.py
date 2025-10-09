from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import math
from bullet import Bullet

class Gun(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 0.07
        self.angle = 0
        self.radius = 65
        self.number_of_bullets = 10
        #175, 100
        with self.canvas:
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source="src/gun1.png"  # ruta a tu imagen PNG
            )
        self.bind(pos=self.update_rect, size=self.update_rect)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self, player_x, player_y):
        self.x = player_x + self.radius * math.cos(self.angle)
        self.y = player_y + self.radius * math.sin(self.angle)
        self.angle += self.velocity

        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

    def shoot(self, Game):
        print("")

