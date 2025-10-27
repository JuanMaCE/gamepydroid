from inputs.devicereader import DeviceReader
from inputs.phone import Phone



class PhoneReader(DeviceReader):
    def createDevice(self) -> Phone:
        return Phone()
