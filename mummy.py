import math
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage


class Mummy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = 1.5

        # Tamaño real de UN frame dentro del PNG
        self.sprite_w = 16
        self.sprite_h = 16

        # Tamaño visible en pantalla (puedes escalarlo)
        self.display_size = 48

        # 🔥 IMPORTANTE: El Widget ahora tiene el tamaño correcto
        self.size = (self.display_size, self.display_size)

        # Cargar textura (64x16 con 4 frames de 16x16)
        self.texture = CoreImage(
            "src/premium asset pack/Premium Undead Animations/Mummified Ritualist/MummifiedRitualist.png"
        ).texture

        # Configuración de animación
        self.total_frames = 4
        self.current_frame = 0

        # Dibujar sprite inicial
        with self.canvas:
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size,
                texture=self.texture
            )

        self.set_frame(0)

        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_interval(self.animate, 0.12)

    def set_frame(self, frame_index):
        """Muestra solo UN frame del spritesheet"""
        frame_x = frame_index * self.sprite_w
        frame_y = 0

        # Normalización (0–1) para OpenGL
        nx = frame_x / self.texture.width
        ny = frame_y / self.texture.height
        nw = self.sprite_w / self.texture.width
        nh = self.sprite_h / self.texture.height

        # 🔥 tex_coords en orden: bottom-left, bottom-right, top-right, top-left
        self.rect.tex_coords = [
            nx, ny,  # bottom-left
            nx + nw, ny,  # bottom-right
            nx + nw, ny + nh,  # top-right
            nx, ny + nh  # top-left
        ]

    def animate(self, dt):
        """Cambia al siguiente frame"""
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.set_frame(self.current_frame)

    def update_rect(self, *args):
        """Actualiza posición cuando se mueve"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    # 🔥 MÉTODOS PARA COLISIONES (hitbox más pequeño 12x12 centrado)
    def get_hitbox(self):
        """Devuelve (x, y, ancho, alto) del hitbox de 12x12 centrado"""
        hitbox_size = 0
        offset = (self.display_size - hitbox_size) / 2
        return (
            self.x + offset,
            self.y + offset,
            hitbox_size,
            hitbox_size
        )

    def collides_with(self, other):
        """Detecta colisión AABB con otro objeto"""
        x1, y1, w1, h1 = self.get_hitbox()

        if hasattr(other, 'get_hitbox'):
            x2, y2, w2, h2 = other.get_hitbox()
        else:
            x2, y2, w2, h2 = other.x, other.y, other.width, other.height

        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)

    def calculate_movement(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        return math.cos(angle) * self.velocity, math.sin(angle) * self.velocity

    def follow_player(self, player_x, player_y):
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.velocity
        self.y += math.sin(angle) * self.velocity

    def set_new_velocity(self, new_ve):
        self.velocity += new_ve