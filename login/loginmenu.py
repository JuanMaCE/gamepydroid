from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle

from doombutton import DoomButton
from doomlabel import DoomLabel


class LoginMenu(Screen):
    def __init__(self, **kwargs):
        super(LoginMenu, self).__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(
                source='src/inital.png',  # ruta de tu imagen
                size=self.size,
                pos=self.pos
            )
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Contenedor principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            padding=[150, 120]
        )

        # Título
        layout.add_widget(DoomLabel(text=""))
        layout.add_widget(DoomLabel(text=""))
        layout.add_widget(Widget(size_hint_y=None, height=30))
        layout.add_widget(Widget(size_hint_y=None, height=30))

        # Botones principales
        btn_login = DoomButton(text="Login", on_release=lambda btn: self.manager.go_to_login_screen())
        btn_register = DoomButton(text="Register", on_release=lambda btn: self.manager.go_to_register())
        btn_unknown = DoomButton(text="Play as Unknown", on_release=lambda btn: self.manager.go_to_main_menu())

        layout.add_widget(btn_login)
        layout.add_widget(btn_unknown)
        layout.add_widget(btn_register)

        # Agregar el layout a la pantalla
        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
