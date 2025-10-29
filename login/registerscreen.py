from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from doombutton import DoomButton
from doomlabel import DoomLabel


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(
                source='src/inital.png',  # ruta de tu imagen
                size=self.size,
                pos=self.pos
            )
            self.bind(size=self._update_bg, pos=self._update_bg)


        layout = BoxLayout(orientation='vertical',
                           spacing=20,
                           padding=[150, 100])

        layout.add_widget(DoomLabel(text=""))
        layout.add_widget(DoomLabel(text=""))
        layout.add_widget(DoomLabel(text=""))


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

        # Confirmar contraseña
        self.confirm_input = TextInput(
            hint_text="Confirm Password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.confirm_input)

        layout.add_widget(Widget(size_hint_y=None, height=20))

        # Botones
        btn_register = DoomButton(text="REGISTER")
        btn_back = DoomButton(text="BACK", on_release=lambda btn: self.manager.go_to_login())

        layout.add_widget(btn_register)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
