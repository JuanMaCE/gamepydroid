from abc import ABC, abstractmethod
from inputs.inputdevice import InputDevice

class DeviceReader(ABC):
    @abstractmethod
    def createDevice(self) -> InputDevice:
        pass

    def getData(self):
        device = self.createDevice()
        return device.readData()
