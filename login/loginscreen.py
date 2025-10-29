from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from doombutton import DoomButton
from doomlabel import DoomLabel


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Fondo oscuro
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Layout principal
        layout = BoxLayout(orientation='vertical',
                           spacing=20,
                           padding=[150, 120])

        layout.add_widget(DoomLabel(text="LOGIN"))

        # Campo usuario
        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.username_input)

        # Campo contraseña
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.password_input)

        # Separador
        layout.add_widget(Widget(size_hint_y=None, height=20))

        # Botones
        btn_login = DoomButton(text="LOGIN")
        btn_back = DoomButton(text="BACK")

        layout.add_widget(btn_login)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
