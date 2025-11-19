from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle
from kivy.core.window import Window


class Player(Widget):
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (30, 45)
        # --- CONFIGURACIÓN DE HITBOX ---
        # Cuanto más grande sea el sprite visual respecto a la hitbox real
        # Ajusta estos valores según tus necesidades:
        self.visual_padding_x = 40  # El sprite será 40px más ancho que la hitbox
        self.visual_padding_y = 20  # El sprite será 20px más alto que la hitbox

        # Animación y control
        self.frame_counter = 0
        self.current_frame = 0
        self.facing_right = True
        self.walk_speed = 5
        self.count_bullets = 0

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
            # Inicializamos el rectángulo visual
            # Nota: La posición y tamaño se calculan en update_rect
            self.rect = Rectangle(
                source=self.sprites_right[0]
            )

        # Vinculamos cambios de posición/tamaño a la actualización visual
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """
        Esta función centra el Sprite (grande) sobre el Widget (hitbox pequeña).
        """
        # 1. Calculamos el tamaño visual (Sprite) sumando el padding
        visual_width = self.width + self.visual_padding_x
        visual_height = self.height + self.visual_padding_y

        # 2. Calculamos la posición visual para centrarlo
        # Restamos la mitad del padding a la posición de la hitbox
        visual_x = self.x - (self.visual_padding_x / 2)
        visual_y = self.y - (self.visual_padding_y / 2)

        # 3. Aplicamos al rectángulo gráfico
        self.rect.pos = (visual_x, visual_y)
        self.rect.size = (visual_width, visual_height)

    def move(self):
        self.y += self.velocity_y
        self.x += self.velocity_x

        # Lógica de colisión con bordes de pantalla (usando la hitbox)
        if self.y < 0:
            self.y = 0
        elif self.top > Window.height:
            self.top = Window.height

        if self.x < 0:
            self.x = 0
        elif self.right > Window.width:
            self.right = Window.width

        self.frame_counter += 1

        # Lógica de animación (sin cambios)
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
            self.rect.source = (
                self.sprites_right[0] if self.facing_right else self.sprites_left[0]
            )

    def add_velocity_x(self, new_velocity):
        self.velocity_x += new_velocity

    def add_velocity_y(self, new_velocity):
        self.velocity_y += new_velocity