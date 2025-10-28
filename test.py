from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation


# Configurar fondo tipo DOOM
Window.clearcolor = (0.05, 0.05, 0.05, 1)  # fondo gris oscuro


class DoomButton(Button):
    def __init__(self, **kwargs):
        super(DoomButton, self).__init__(**kwargs)
        self.font_size = '30sp'
        self.bold = True
        self.color = (1, 0.85, 0, 1)  # texto dorado
        self.background_normal = ''  # elimina textura por defecto
        self.background_color = (0.4, 0, 0, 1)  # rojo oscuro base
        self.size_hint = (1, 0.3)
        self.border = (8, 8, 8, 8)
        self.bind(on_enter=self.on_hover, on_leave=self.on_unhover)

    def on_hover(self, *args):
        # Efecto de brillo infernal
        Animation(background_color=(0.8, 0.1, 0.1, 1), duration=0.2).start(self)

    def on_unhover(self, *args):
        Animation(background_color=(0.4, 0, 0, 1), duration=0.2).start(self)


class DoomLabel(Label):
    def __init__(self, **kwargs):
        super(DoomLabel, self).__init__(**kwargs)
        self.font_size = '60sp'
        self.bold = True
        self.color = (1, 0.3, 0, 1)  # rojo lava
        self.outline_color = (0, 0, 0, 1)
        self.outline_width = 2


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        # Fondo tipo metal oxidado (gradiente simulado)
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical',
                           spacing=25,
                           padding=[150, 120])

        # Título
        layout.add_widget(DoomLabel(text="ATTACK OF MOMMIES"))

        # Espaciador
        layout.add_widget(Widget(size_hint_y=None, height=30))

        # Botones
        btn_play = DoomButton(text="PLAY")
        btn_options = DoomButton(text="OPTIONS")
        btn_ranking = DoomButton(text="RANKING")

        layout.add_widget(btn_play)
        layout.add_widget(btn_options)
        layout.add_widget(btn_ranking)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos


class DoomApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        return sm


if __name__ == '__main__':
    DoomApp().run()
