from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
import random

from bullet import Bullet
from gun import Gun
from mummy import Mummy
from player import Player


class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 450)
        self.level_passed = False
        # --- Fondo ---
        with self.canvas.before:
            self.bg = Rectangle(source='src/fondo.jpg', pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # --- Variables del juego ---
        self.level = 1
        self.size_player = 60
        self.size_enemy = 100
        self.pos_initial_x = 400
        self.pos_initial_y = 225
        self.count_of_bulls = 5
        self.player = Player(
            size=(self.size_player, self.size_player),
            pos=(self.pos_initial_x, self.pos_initial_y),
            size_hint = (None, None)
        )

        self.radius = 65
        self.gun = Gun(
            size=(50, 20),
            pos=(self.pos_initial_x + self.radius, self.pos_initial_y),
            size_hint = (None, None)
        )

        self.enemies = []
        self.bullets = []
        self.bullets_to_agregate = []


        # --- Crear enemigos ---
        for j in range(5):
            rangos_x = [(0, 50), (925, 975)]
            inicio, fin = random.choice(rangos_x)
            position_x = random.randint(inicio, fin)

            rangos_y = [(0, 55), (430, 503)]
            inicio, fin = random.choice(rangos_y)
            position_y = random.randint(inicio, fin)

            enemy = Mummy(
                size=(self.size_enemy, self.size_enemy),
                pos=(position_x, position_y),
                size_hint = (None, None)
            )

            self.enemies.append(enemy)
            self.add_widget(enemy)

        # --- Agregar jugador y arma ---
        self.add_widget(self.gun)
        self.add_widget(self.player)


        # --- Actualización ---
        Clock.schedule_interval(self.update, 1/120)
        Clock.schedule_interval(self.generate_bullet, 5)

        # --- Controles ---
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)




    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size


    def update(self, dt):
        self.gun.move(self.player.x, self.player.y)
        self.player.move()
        # este es para ver si las balas impactan
        if self.bullets:
            for bullet in self.bullets:
                bullet.move(self.gun.angle)
                for enemy in self.enemies:
                    if bullet.collide_widget(enemy):
                        self.remove_widget(enemy)
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.remove_widget(bullet)
                        break

        # este es para ver si hay colisión con el personaje
        if self.enemies:
            for enemy in self.enemies:
                value = self.is_caught(enemy)
                enemy.follow_player(self.player.x, self.player.y)
                if self.player.collide_widget(enemy):
                    self.remove_widget(self.player)
                    self.remove_widget(enemy)
                    self.remove_widget(self.gun)
                    Clock.schedule_once(self.go_to_finish, 0.1)
                    print("has muerto")

        print("enemies: ", len(self.enemies))
        print("bulls: ", self.count_of_bulls)


        if self.bullets_to_agregate:
            for bullet in self.bullets_to_agregate:
                if bullet.collide_widget(self.player):
                    self.count_of_bulls += 1
                    self.bullets_to_agregate.remove(bullet)
                    self.remove_widget(bullet)

    def on_touch_down(self, touch):
        pass



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
            self.shoot_bullet()
        elif key == 120:
            self.player.recolect_items()

    def on_key_up(self, window, key, *args):
        self.player.velocity_y = 5
        self.player.velocity_x = 5
        self.player.velocity_y = 0
        self.player.velocity_x = 0

    def shoot_bullet(self):
        if self.count_of_bulls:
            bullet = Bullet(
                size=(15, 15),
                pos=(self.gun.x, self.gun.y),
                size_hint = (None, None)
            )
            self.count_of_bulls -= 1
            self.bullets.append(bullet)
            self.add_widget(bullet)

    #agregar interfaz
    def is_caught(self, enemie: Mummy):
        return enemie.collide_widget(self.player)

    def go_to_finish(self, dt):
        self.manager.current = "finish"

    def generate_bullet(self, dt):
        size = 30
        x = random.randint(0, 975)
        y = random.randint(0, 505)
        new_bullet = Bullet(
            size=(size, size),
            pos=(x, y),
            size_hint=(None, None)
        )
        self.add_widget(new_bullet)
        self.bullets_to_agregate.append(new_bullet)
