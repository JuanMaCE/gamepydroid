from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

class EnemyRenderer:
    """Implementación: cómo se dibuja un enemigo."""
    def __init__(self, texture_path, sprite_w, sprite_h, display_size, total_frames):
        self.texture = CoreImage(texture_path).texture
        self.sprite_w = sprite_w
        self.sprite_h = sprite_h
        self.display_size = display_size
        self.total_frames = total_frames
        self.current_frame = 0
        self.color = (1, 1, 1, 1)  # color inicial blanco
        self.color_instruction = None
        self.rect = None

    def attach(self, widget):
        widget.size = (self.display_size, self.display_size)

        widget.canvas.clear()
        with widget.canvas:
            self.color_instruction = Color(*self.color)
            self.rect = Rectangle(
                pos=widget.pos,
                size=widget.size,
                texture=self.texture
            )

        widget.bind(pos=self.update_rect, size=self.update_rect)
        self.set_frame(0)
        Clock.schedule_interval(self.animate, 0.12)

    def set_color(self, rgba):
        self.color = rgba
        if self.color_instruction:
            self.color_instruction.rgba = rgba

    def update_rect(self, widget, *args):
        if self.rect:
            self.rect.pos = widget.pos
            self.rect.size = widget.size

    def set_frame(self, frame_index):
        if not self.rect:
            return
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
