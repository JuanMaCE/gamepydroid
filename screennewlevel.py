from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class ScreenNewLevel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self._transition_event = None

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.label = Label(
            text=f"Nivel... {self.level}",
            font_size='40sp',
            halign='center',
            valign='middle'
        )
        self.add_widget(self.label)

    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def set_level(self, new_level: int):

        self.level = new_level
        self.label.text = f"Nivel... {self.level}"


        if self._transition_event:
            self._transition_event.cancel()

        self._transition_event = Clock.schedule_once(self.go_to_game, 2)

    def go_to_game(self, dt):
        if self.manager and self.manager.has_screen("game"):
            game_screen = self.manager.get_screen("game")
            game_screen.generate_game(self.level)

            self.manager.current = "game"
        else:
            print("Error: La pantalla 'game' no fue encontrada.")

    def on_leave(self, *args):
        if self._transition_event:
            self._transition_event.cancel()
            self._transition_event = None
