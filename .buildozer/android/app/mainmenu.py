from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.metrics import dp
from doombutton import DoomButton
from doomlabel import DoomLabel

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.id = None

        # Fondo que se ajusta a toda la pantalla
        self.bg = Image(
            source='src/inital.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.add_widget(self.bg)

        # Layout principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(20)],  # padding proporcional
            size_hint=(1, 1)
        )

        # Espacio superior
        layout.add_widget(Widget(size_hint_y=0.1))

        # Título o label superior
        layout.add_widget(DoomLabel(text="GamePyDroid", size_hint_y=0.1))

        # Espacio entre título y botones
        layout.add_widget(Widget(size_hint_y=0.1))

        # Botones con tamaño relativo
        btn_play = DoomButton(
            text="PLAY",
            size_hint_y=0.15,
            on_release=lambda btn: self.manager.go_to_play(self.id)
        )
        btn_options = DoomButton(
            text="OPTIONS",
            size_hint_y=0.15
        )
        btn_ranking = DoomButton(
            text="RANKING",
            size_hint_y=0.15,
            on_release=lambda btn: self.manager.go_to_ranking()
        )

        layout.add_widget(btn_play)
        layout.add_widget(btn_options)
        layout.add_widget(btn_ranking)

        # Espacio inferior
        layout.add_widget(Widget(size_hint_y=0.2))

        self.add_widget(layout)

    def set_new_id(self, id: int | None):
        self.id = id
