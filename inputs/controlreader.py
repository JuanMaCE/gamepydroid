from inputs.devicereader import DeviceReader
from inputs.controller import Controller


class ControlReader(DeviceReader):
    def createDevice(self) -> Controller:
        return Controller()