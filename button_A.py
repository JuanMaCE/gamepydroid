from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ButtonA(ButtonBehavior, Widget):
    def __init__(self, letter='A', size=80, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (size, size)
        self.pos = [650, 150]
        with self.canvas:
            Color(0.12, 0.56, 0.86, 0.5)  # color azul (r,g,b)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.label = Label(text=letter, color=(1,1,1,0.1), bold=True, font_size=size*0.45,
                           size_hint=(None,None), size=self.size, pos=self.pos, halign='center', valign='middle')
        self.add_widget(self.label)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

    def clicked(self):
        pass