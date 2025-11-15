from kivy.core.window import Window
from inputs.inputdevice import InputDevice


class Keyboard(InputDevice):
    def __init__(self):
        # Vinculamos la detección de teclas
        Window.bind(on_key_down=self._on_key_down)
        Window.bind(on_key_up=self._on_key_up)

        self.data = {
            "x": 0,
            "y": 0,
            "z": 0
        }


    def _on_key_down(self, window, key, scancode, codepoint, modifiers):

        if key == 100 or key == 275:
            self.data["x"] = 5
        elif key == 97 or key == 276:
            self.data["x"] = -5
        elif key == 119 or key == 273:
            self.data["y"] = 5
        elif key == 115 or key == 274:
            self.data["y"] = -5
        elif key == 122:
            self.data["z"] = 1

    def _on_key_up(self, window, key, scancode):
        if key in (273, 119):
            self.data["y"] = 0
        elif key in (274, 115):
            self.data["y"] = 0
        elif key in (275, 100):
            self.data["x"] = 0
        elif key in (276, 97):
            self.data["x"] = 0
        elif key == 122:
            self.data["z"] = 0


    def readData(self) -> dict[str, int]:
        return self.data
