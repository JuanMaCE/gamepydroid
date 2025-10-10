from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import  Rectangle
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage




class Player(Widget):
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Carga la imagen como textura
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source="src/ch1.png"  # ruta a tu imagen PNG
            )

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

    def shoot(self):
        print("pium pium")

    def recolect_items(self):
        print("item recogido")