from random import randint
from PyQt6.uic.pyuic import generate
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from numpy.matlib import empty
from player import Player
from mummy import Mummy
from gun import Gun
from bullet import Bullet
import random




class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self.player = Player(size=(50, 50), pos=(200, 100))
        self.radius = 65
        self.gun = Gun(size=(50, 20), pos=(200 + self.radius, 100 ))
        self.enemies = []
        self.bullets = []

        for j in range(5):
            position_x = random.randint(0, 800)
            position_y = random.randint(0, 450)

            enemy = Mummy(size=(50, 50), pos=(position_x, position_y))
            self.enemies.append(enemy)
            self.add_widget(enemy)

        self.add_widget(self.gun)
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1/120)

        Window.size = (800, 450)

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def update(self, dt):


        self.gun.move(self.player.x, self.player.y)
        self.player.move()

        if self.bullets != []:
            for bullet in self.bullets:
                bullet.move(self.gun.angle)
                for enemy in self.enemies:
                    if bullet.collide_widget(enemy):
                        self.remove_widget(enemy)


    def on_touch_down(self, touch):
        print(touch.y)
        print(touch.x)



    def on_touch_up(self, touch):
        self.player.velocity_y = 0

    def on_key_down(self, window, key, *args):

        if key == 273:
            self.player.velocity_y = 5
        elif key == 274:
            self.player.velocity_y = -5
        elif key == 275:
            self.player.velocity_x = 5
        elif key == 276:
            self.player.velocity_x = -5
        elif key == 122:
            self.generate_bullet()
        elif key == 120:
            self.player.recolect_items()

    def on_key_up(self, window, key, *args):
        self.player.velocity_y = 5
        self.player.velocity_x = 5
        self.player.velocity_y = 0
        self.player.velocity_x = 0

    def generate_bullet(self):
        bullet = Bullet(size=(5, 5), pos=(self.gun.x, self.gun.y))
        self.bullets.append(bullet)
        self.add_widget(bullet)
