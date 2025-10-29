from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from doombutton import DoomButton
from doomlabel import DoomLabel


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(
                source='src/inital.png',  # ruta de tu imagen
                size=self.size,
                pos=self.pos
            )
            self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical',
                           spacing=25,
                           padding=[150, 120])

        layout.add_widget(DoomLabel(text=""))

        layout.add_widget(Widget(size_hint_y=None, height=30))

        # Botones
        btn_play = DoomButton(text="PLAY",  on_release=lambda btn: self.manager.go_to_play())
        btn_options = DoomButton(text="OPTIONS")
        btn_ranking = DoomButton(text="RANKING")

        layout.add_widget(btn_play)
        layout.add_widget(btn_options)
        layout.add_widget(btn_ranking)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

