from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

class EnemyRenderer:
    """Implementación: cómo se dibuja un enemigo."""
    def __init__(self, texture_path, sprite_w, sprite_h, display_size, total_frames):
        self.texture = CoreImage(texture_path).texture

        # Animación
        self.sprite_w = sprite_w
        self.sprite_h = sprite_h
        self.display_size = display_size
        self.total_frames = total_frames
        self.current_frame = 0

    def attach(self, widget):
        """Crea el dibujo dentro del widget."""
        widget.size = (self.display_size, self.display_size)

        with widget.canvas:
            self.rect = Rectangle(
                pos=widget.pos,
                size=widget.size,
                texture=self.texture
            )

        widget.bind(pos=self.update_rect, size=self.update_rect)
        self.set_frame(0)

        Clock.schedule_interval(self.animate, 0.12)

    def update_rect(self, widget, *args):
        self.rect.pos = widget.pos
        self.rect.size = widget.size

    def set_frame(self, frame_index):
        frame_x = frame_index * self.sprite_w
        frame_y = 0

        nx = frame_x / self.texture.width
        ny = frame_y / self.texture.height
        nw = self.sprite_w / self.texture.width
        nh = self.sprite_h / self.texture.height

        self.rect.tex_coords = [
            nx, ny,
            nx + nw, ny,
            nx + nw, ny + nh,
            nx, ny + nh
        ]

    def animate(self, dt):
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.set_frame(self.current_frame)
