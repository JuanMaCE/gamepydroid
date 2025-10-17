from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.core.window import Window
import math
from bullet import Bullet

class Gun(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 0.06
        self.angle = 0
        self.radius = 65
        self.number_of_bullets = 10
        #175, 100

        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=0, origin=self.center)
            print(self.center)
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source="src/gun1.png"  # ruta a tu imagen PNG
            )
            PopMatrix()
        self.bind(pos=self.update_rect, size=self.update_rect)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self, player_x, player_y):
        self.x = player_x + self.radius * math.cos(self.angle)
        self.y = player_y + self.radius * math.sin(self.angle)

        # Actualiza el ángulo orbital
        self.angle += self.velocity
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

        # Calcular el ángulo de orientación hacia el jugador
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        rotation_angle = math.degrees(math.atan2(dy, dx))

        self.rotation.origin = self.center
        self.rotation.angle = rotation_angle + 180

    def shoot(self, Game):
        print("")

