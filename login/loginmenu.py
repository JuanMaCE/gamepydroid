from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.metrics import dp
from doombutton import DoomButton
from doomlabel import DoomLabel

class LoginMenu(Screen):
    def __init__(self, **kwargs):
        super(LoginMenu, self).__init__(**kwargs)

        # Fondo que ocupa toda la pantalla
        self.bg = Image(
            source='src/inital.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.add_widget(self.bg)

        # Layout principal, centrado verticalmente
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(30),          # espacio grande entre botones
            padding=[dp(50), dp(50)],
            size_hint=(0.8, 0.7),    # ocupa 80% ancho y 70% alto
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Título grande tipo arcade
        layout.add_widget(DoomLabel(
            text=" ",
            font_size=dp(40),
            size_hint_y=None,
            height=dp(60)
        ))

        # Espacio extra
        layout.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Botones grandes tipo arcade
        btn_login = DoomButton(
            text="Login",
            size_hint_y=None,
            height=dp(70),
            on_release=lambda btn: self.manager.go_to_login_screen()
        )
        btn_unknown = DoomButton(
            text="Play as Unknown",
            size_hint_y=None,
            height=dp(70),
            on_release=lambda btn: self.manager.go_to_main_menu(None)
        )
        btn_register = DoomButton(
            text="Register",
            size_hint_y=None,
            height=dp(70),
            on_release=lambda btn: self.manager.go_to_register()
        )

        layout.add_widget(btn_login)
        layout.add_widget(btn_unknown)
        layout.add_widget(btn_register)

        self.add_widget(layout)
