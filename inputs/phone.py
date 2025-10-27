from inputs.inputdevice import InputDevice


class Phone(InputDevice):
    def readData(self):
        return "Datos del phone"