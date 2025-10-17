from kivy.graphics import Color, Ellipse
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty

class ButtonB(ButtonBehavior, Widget):

    outline_color = ListProperty([1, 1, 1, 0.4])
    fill_color_normal = ListProperty([1, 1, 1, 0.2])
    fill_color_down = ListProperty([1, 1, 1, 0.5])
    text = StringProperty('B')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos = [800, 150]
        with self.canvas:
            self.outline_canvas_color = Color(rgba=self.outline_color)
            self.outline = Ellipse(size=self.size, pos=self.pos)

            self.fill_canvas_color = Color(rgba=self.fill_color_normal)
            self.fill = Ellipse(size=(self.width * 0.9, self.height * 0.9), pos=self.pos)

        # 3. Etiqueta con la letra
        self.label = Label(
            text=self.text,
            bold=True,
            font_size=self.height * 0.5,
            color=(1, 1, 1, 1),
            pos=self.pos
        )
        self.add_widget(self.label)




    def _update(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

