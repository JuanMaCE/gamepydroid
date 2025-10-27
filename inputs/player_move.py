from bulletmanager import BulletManager
from gun import Gun
from inputs.controlreader import ControlReader
from inputs.keyboardreader import KeyboardReader
from inputs.phone import Phone
from inputs.phonereader import PhoneReader
from player import Player


class PlayerMove:
    def __init__(self):
        self.reader = ControlReader()
        self.reader1 = KeyboardReader()
        self.reader2 = PhoneReader()
        self.reads = [self.reader, self.reader2, self.reader1]
        self.phone_instance = Phone()

    def setup_phone_controls(self, parent_widget):
        self.phone_instance.set_parent_widget(parent_widget)
        self.reader2.set_phone(self.phone_instance)  # Conectar la misma instancia

    def returnPhoneReader(self):
        return self.reader2

    def move(self, player: Player, gun: Gun, bullets: BulletManager, addWidget):
        data = self.reader2.getData()
        if data["z"] == 1:
            bullets.shoot_bullet(
                (gun.center_x, gun.center_y),
                addWidget
            )
            self.phone_instance.data["z"] = 0

        player.velocity_x = data["x"]
        player.velocity_y = data["y"]
        player.move()
        gun.move(player.x, player.y)