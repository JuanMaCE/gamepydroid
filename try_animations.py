import random
from abc import ABC, abstractmethod
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage


# ================= INTERFAZ =================
class IAnimated(ABC):
    @abstractmethod
    def animate(self, dt):
        """Avanza la animación de frames"""
        pass

    @abstractmethod
    def update_rect(self, *args):
        """Actualiza la posición y tamaño del rectángulo"""
        pass

    @abstractmethod
    def start(self, parent):
        """Agrega la animación al parent y activa el timer"""
        pass


# ================= ANIMATED SPRITE =================
class AnimatedSprite(Widget, IAnimated):
    def __init__(self, texture_path, total_frames=4, display_size=128, duration=3, **kwargs):
        super().__init__(**kwargs)
        self.sprite_w = 16  # ancho de un frame en el PNG
        self.sprite_h = 16  # alto de un frame
        self.display_size = display_size
        self.size = (display_size, display_size)

        self.texture = CoreImage(texture_path).texture
        self.total_frames = total_frames
        self.current_frame = 0
        self.duration = duration  # tiempo en pantalla
        self.time_elapsed = 0

        # Dibujar el primer frame
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)
        self.set_frame(0)

        # Actualizar cuando la posición o tamaño cambie
        self.bind(pos=self.update_rect, size=self.update_rect)

    # ---------------- FRAME ANIMATION ----------------
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

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # ---------------- CONTROL DE DURACIÓN ----------------
    def _check_duration(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed >= self.duration:
            if self.parent:
                self.parent.remove_widget(self)
            Clock.unschedule(self.animate_event)
            Clock.unschedule(self.timer_event)

    # ---------------- START ANIMATION ----------------
    def start(self, parent, pos=None, full_screen=False):
        """Agrega al parent y comienza animación y timer"""
        if full_screen:
            self.size = parent.size
            self.pos = parent.pos
        else:
            if pos is None:
                # Posición aleatoria
                self.pos = (random.randint(0, parent.width - self.display_size),
                            random.randint(0, parent.height - self.display_size))
            else:
                self.pos = pos

        parent.add_widget(self)
        self.animate_event = Clock.schedule_interval(self.animate, 0.12)
        self.timer_event = Clock.schedule_interval(self._check_duration, 0.1)


# ================= FACTORY =================
class AnimationFactory:
    @staticmethod
    def create_vampire(parent, texture_path, display_size=128, duration=3, full_screen=False, pos=None):
        sprite = AnimatedSprite(texture_path, total_frames=4, display_size=display_size, duration=duration)
        sprite.start(parent, pos=pos, full_screen=full_screen)
        return sprite

    @staticmethod
    def create_animation(parent, texture_path, total_frames=4, display_size=128, duration=3,
                         full_screen=False, pos=None):
        """Método genérico para cualquier sprite animado"""
        sprite = AnimatedSprite(texture_path, total_frames=total_frames, display_size=display_size, duration=duration)
        sprite.start(parent, pos=pos, full_screen=full_screen)
        return sprite


# ================= EJEMPLO DE USO =================
# Dentro de tu clase Game, podrías usarlo así:
def show_vampires(self):
    # Primer vampiro: aparece 3 segundos
    AnimationFactory.create_vampire(
        parent=self,
        texture_path="src/vampiro1.png",
        display_size=128,
        duration=3
    )

    # Segundo vampiro: aparece 5 segundos, full screen
    Clock.schedule_once(lambda dt: AnimationFactory.create_vampire(
        parent=self,
        texture_path="src/vampiro2.png",
        display_size=self.width,
        duration=5,
        full_screen=True
    ), 3.1)  # después del primer vampiro
