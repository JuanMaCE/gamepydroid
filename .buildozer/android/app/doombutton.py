from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import ListProperty

Window.clearcolor = (0.1, 0, 0, 1)


class DoomButton(Button):
    normal_bg_color = ListProperty([0.4, 0, 0, 0])
    hover_bg_color = ListProperty([0.8, 0.1, 0.1, 0.3])

    def __init__(self, **kwargs):
        super(DoomButton, self).__init__(**kwargs)
        self.font_size = '18sp'
        self.bold = True
        self.color = (1, 0.85, 0, 1)
        self.background_normal = ''
        self.background_color = self.normal_bg_color[:]
        self.size_hint = (None, None)
        self.size = (120, 50)
        self.border = (8, 8, 8, 8)
        self.bind(on_enter=self.on_hover, on_leave=self.on_unhover)

    def on_hover(self, *args):
        Animation(background_color=self.hover_bg_color, duration=0.2).start(self)

    def on_unhover(self, *args):
        Animation(background_color=self.normal_bg_color, duration=0.2).start(self)

