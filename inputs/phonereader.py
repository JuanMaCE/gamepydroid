from inputs.devicereader import DeviceReader
from inputs.phone import Phone


class PhoneReader:
    def __init__(self):
        self.phone = None

    def set_phone(self, phone_instance):
        self.phone = phone_instance

    def getData(self):
        if self.phone:
            return self.phone.readData()
        else:
            print("ERROR: Phone not set in PhoneReader")
            return {"x": 0, "y": 0, "z": 0}
