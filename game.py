from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from player import Player




class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(size=(50, 50), pos=(175, 100))
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1/60)

        Window.size = (800, 450)

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def update(self, dt):
        self.player.move()

    def on_touch_down(self, touch):
        if touch.y > self.player.y:
            self.player.velocity_y = 5
        else:
            self.player.velocity_y = -5

    def on_touch_up(self, touch):
        self.player.velocity_y = 0

    def on_key_down(self, window, key, *args):
        print(key)

        if key == 273:
            self.player.velocity_y = 5
        elif key == 274:
            self.player.velocity_y = -5
        elif key == 275:
            self.player.velocity_x = 5
        elif key == 276:
            self.player.velocity_x = -5

    def on_key_up(self, window, key, *args):
        self.player.velocity_y = 0
        self.player.velocity_x = 0