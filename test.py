from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, PushMatrix, PopMatrix, Translate, Scale
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics.texture import Texture
import numpy as np

Window.size = (800, 600)

CHUNK_PX = 256
LOAD_RADIUS = 1
MOVE_SPEED = 200  # px/segundo

class MapWidget(Widget):
    player_x = NumericProperty(0)
    player_y = NumericProperty(0)
    zoom = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keys_pressed = set()
        self.rects = {}
        self.chunks = {}

        # Cámara
        with self.canvas.before:
            PushMatrix()
            self._translate = Translate(0, 0, 0)
            self._scale = Scale(1.0)
        with self.canvas.after:
            PopMatrix()

        # Player (simple rectángulo rojo)
        self.player_size = 20

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        Window.bind(on_mouse_scroll=self.on_mouse_scroll)

        self.player_x = 400
        self.player_y = 300

        Clock.schedule_interval(self.update, 1 / 60.0)

    def world_to_chunk(self, x, y):
        gx = int(x // CHUNK_PX)
        gy = int(y // CHUNK_PX)
        return gx, gy

    def load_chunk_texture(self, gx, gy):
        key = (gx, gy)
        if key in self.chunks:
            return self.chunks[key]

        tex = Texture.create(size=(CHUNK_PX, CHUNK_PX))
        r = (abs(gx * 70) % 255)
        g = (abs(gy * 60) % 255)
        b = ((gx + gy) * 30) % 255
        arr = np.zeros((CHUNK_PX, CHUNK_PX, 3), dtype='uint8')
        arr[..., 0] = r
        arr[..., 1] = g
        arr[..., 2] = b
        tex.blit_buffer(arr.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        tex.flip_vertical()
        self.chunks[key] = tex
        return tex

    def manage_visible_chunks(self):
        pgx, pgy = self.world_to_chunk(self.player_x, self.player_y)
        should_be = set()
        for dx in range(-LOAD_RADIUS, LOAD_RADIUS + 1):
            for dy in range(-LOAD_RADIUS, LOAD_RADIUS + 1):
                should_be.add((pgx + dx, pgy + dy))

        for key in should_be:
            if key not in self.rects:
                gx, gy = key
                tex = self.load_chunk_texture(gx, gy)
                x = gx * CHUNK_PX
                y = gy * CHUNK_PX
                with self.canvas:
                    Rectangle(texture=tex, pos=(x, y), size=(CHUNK_PX, CHUNK_PX))
                self.rects[key] = True

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 270:  # tecla +
            self.zoom *= 1.1
        elif key == 269:  # tecla -
            self.zoom /= 1.1
        else:
            self.keys_pressed.add(key)

    def on_key_up(self, window, key, *args):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_scroll(self, window, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.zoom *= 1.1
        elif scroll_y < 0:
            self.zoom /= 1.1

    def update(self, dt):
        # Movimiento del jugador
        vx, vy = 0, 0
        if 119 in self.keys_pressed or 273 in self.keys_pressed:  # W o flecha arriba
            vy += 1
        if 115 in self.keys_pressed or 274 in self.keys_pressed:  # S o flecha abajo
            vy -= 1
        if 97 in self.keys_pressed or 276 in self.keys_pressed:   # A o flecha izq
            vx -= 1
        if 100 in self.keys_pressed or 275 in self.keys_pressed:  # D o flecha der
            vx += 1

        self.player_x += vx * MOVE_SPEED * dt
        self.player_y += vy * MOVE_SPEED * dt

        # Actualizar chunks visibles
        self.manage_visible_chunks()

        # Actualizar cámara
        self._scale.x = self._scale.y = self.zoom
        self._translate.x = -self.player_x * self.zoom + self.width / 2
        self._translate.y = -self.player_y * self.zoom + self.height / 2

        # Dibujar jugador
        self.canvas.remove_group('player')
        with self.canvas:
            Color(1, 0, 0, 1, group='player')
            Rectangle(pos=(self.player_x - self.player_size / 2,
                           self.player_y - self.player_size / 2),
                      size=(self.player_size, self.player_size),
                      group='player')


class ZoomMapApp(App):
    def build(self):
        return MapWidget()


if __name__ == "__main__":
    ZoomMapApp().run()
