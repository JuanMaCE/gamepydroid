from inputs.devicereader import DeviceReader
from inputs.controller import Controller


class ControlReader(DeviceReader):
    def __init__(self):
        self.device = Controller()

    def createDevice(self) -> Controller:
        return self.device
