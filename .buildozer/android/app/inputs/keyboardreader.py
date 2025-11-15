from inputs.devicereader import DeviceReader
from inputs.keyboard import Keyboard

class KeyboardReader(DeviceReader):
    def __init__(self):
        self.device = Keyboard()

    def createDevice(self) -> Keyboard:
        return self.device
