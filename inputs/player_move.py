from inputs.devicereader import DeviceReader
from inputs.keyboardreader import KeyboardReader
from inputs.phonereader import PhoneReader
from inputs.controlreader import ControlReader
from player import Player

class PlayerMove:
    def __init__(self):
        self.reader = ControlReader()
        self.reader1 = KeyboardReader()
        #self.reader = KeyboardReader()

    def move(self, player: Player):
        data = self.reader.getData()
        print(data)
        player.velocity_x = data["x"]
        player.velocity_y = data["y"]
        player.move()
