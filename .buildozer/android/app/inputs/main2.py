from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from keyboardreader import KeyboardReader


class VentanaFlechas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 30
        self.spacing = 20

        self.label = Label(
            text="Presiona una tecla de flecha o WASD o Z",
            font_size=26
        )
        self.add_widget(self.label)
        self.reader = KeyboardReader()
        # Actualizar el texto en pantalla cada frame
        from kivy.clock import Clock
        Clock.schedule_interval(self.update_text, 0.1)

    def update_text(self, dt):

        key_text = self.reader.getData()
        print(self.reader.getData())
        if key_text:
            self.label.text = f"Acción: {key_text}"


class TecladoApp(App):
    def build(self):
        return VentanaFlechas()


if __name__ == "__main__":
    TecladoApp().run()
