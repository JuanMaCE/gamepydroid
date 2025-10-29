from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.text_input = TextInput(
            hint_text="Escribe aquí...",
            multiline=False,  # solo una línea
            font_size=24
        )
        layout.add_widget(self.text_input)

        submit_btn = Button(text="Aceptar", size_hint=(1, 0.2))
        submit_btn.bind(on_press=self.submit)
        layout.add_widget(submit_btn)

        self.add_widget(layout)

    def submit(self, instance):
        print("Palabra ingresada:", self.text_input.text)
        self.text_input.text = ""  # limpiar después de leer

class JuegoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name="input"))
        return sm

if __name__ == "__main__":
    JuegoApp().run()
