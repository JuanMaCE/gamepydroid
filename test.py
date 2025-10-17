from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.core.window import Window

class RotatingImage(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(origin=(Window.width / 2, Window.height / 2))
            self.rect = Rectangle(source="tu_imagen.png",
                                  pos=(Window.width / 4, Window.height / 4),
                                  size=(300, 300))
            PopMatrix()

        # Actualizar cada frame
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.rotation.angle += 1  # aumenta el ángulo cada frame

class RotApp(App):
    def build(self):
        return RotatingImage()

RotApp().run()
