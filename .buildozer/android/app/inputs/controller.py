from inputs.inputdevice import InputDevice
from kivy.core.window import Window




class Controller(InputDevice):
    def __init__(self):
        self.data = {
            "x": 0,
            "y": 0,
            "z": 0,
            "a": 0
        }

        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_button_down)


    def on_joy_axis(self, window, stickid, axisid, value):
        if axisid == 0:
            if value > 0:
                self.data["x"] = 5
            if value == 0:
                self.data["x"] = 0
            if value < 0:
                self.data["x"] = -5
        elif axisid == 1:
            if value > -1:
                self.data["y"] = -5
            if value == -1:
                self.data["y"] = 0
            if value < -1:
                self.data["y"] = 5
        else:
            self.data["x"] = 0
            self.data["y"] = 0

    def on_button_down(self, window, stickid, buttonid):
        if buttonid == 1:
            self.data["z"] = 1
        if buttonid == 3:
            self.data["a"] = 1

    def readData(self) -> dict[str, int]:
        return self.data

