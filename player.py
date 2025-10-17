from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle
from kivy.core.window import Window


class Player(Widget):
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Animación y control
        self.frame_counter = 0
        self.current_frame = 0
        self.facing_right = True
        self.walk_speed = 6

        # Listas de sprites
        self.sprites_right = [
            "src/characters/popis-default.png",
            "src/characters/popis-derecha.png"
        ]
        self.sprites_left = [
            "src/characters/popis-default-left.png",
            "src/characters/popis-left.png"
        ]

        with self.canvas:
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                source=self.sprites_right[0]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self):
        # Movimiento físico
        self.y += self.velocity_y
        self.x += self.velocity_x

        # Mantener dentro de la ventana
        if self.y < 0:
            self.y = 0
        elif self.top > Window.height:
            self.top = Window.height

        if self.x < 0:
            self.x = 0
        elif self.right > Window.width:
            self.right = Window.width

        # Animación de movimiento
        self.frame_counter += 1

        if self.velocity_x > 0:
            self.facing_right = True
            if self.frame_counter % self.walk_speed == 0:
                self.current_frame = (self.current_frame + 1) % len(self.sprites_right)
                self.rect.source = self.sprites_right[self.current_frame]

        elif self.velocity_x < 0:
            self.facing_right = False
            if self.frame_counter % self.walk_speed == 0:
                self.current_frame = (self.current_frame + 1) % len(self.sprites_left)
                self.rect.source = self.sprites_left[self.current_frame]

        else:
            # Quieto — sprite por defecto
            self.rect.source = (
                self.sprites_right[0] if self.facing_right else self.sprites_left[0]
            )

    def add_velocity_x(self, new_velocity):
        self.velocity_x += new_velocity

    def add_velocity_y(self, new_velocity):
        self.velocity_y += new_velocity

    def shoot(self):
        print("pium pium")

    def recolect_items(self):
        print("item recogido")
