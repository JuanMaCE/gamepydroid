from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

from doombutton import DoomButton
from doomlabel import DoomLabel


class LoginMenu(Screen):
    def __init__(self, **kwargs):
        super(LoginMenu, self).__init__(**kwargs)

        # Fondo gris oscuro
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Contenedor principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            padding=[150, 120]
        )

        # Título
        layout.add_widget(DoomLabel(text="LOGIN"))

        layout.add_widget(Widget(size_hint_y=None, height=30))

        # Botones principales
        btn_login = DoomButton(text="LOGIN")
        btn_guest = DoomButton(text="PLAY AS UNKNOWN")
        btn_register = DoomButton(text="REGISTER")

        layout.add_widget(btn_login)
        layout.add_widget(btn_guest)
        layout.add_widget(btn_register)

        # Agregar el layout a la pantalla
        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
