from abc import ABC, abstractmethod


class InputDevice(ABC):
    @abstractmethod
    def readData(self):
        pass