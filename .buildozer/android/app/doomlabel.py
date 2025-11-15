from kivy.app import App
from kivy.uix.label import Label



class DoomLabel(Label):
    def __init__(self, **kwargs):
        super(DoomLabel, self).__init__(**kwargs)
        self.font_size = '60sp'
        self.bold = True
        self.color = (1, 0.3, 0, 1)  # rojo lava
        self.outline_color = (0, 0, 0, 1)
        self.outline_width = 2