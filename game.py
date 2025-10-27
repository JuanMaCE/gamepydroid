from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Rectangle
import random
from kivy.core.window import Window
from bullet import Bullet
from gun import Gun
from inputs.keyboardreader import KeyboardReader
from mummy import Mummy
from player import Player
from button_A import ButtonA
from button_B import ButtonB
from inputs.player_move import PlayerMove

class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self.level_passed = False

        self.update_event = None
        self.bullet_gen_event = None

        with self.canvas.before:
            self.bg = Rectangle(source='src/fondo.png', pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.size_player = 70
        self.size_enemy = 100
        self.pos_initial_x = 400
        self.pos_initial_y = 225
        self.count_of_bulls = 5

        self.enemies = []
        self.bullets = []
        self.bullets_to_agregate = []

        self.player = Player(
            size=(self.size_player, self.size_player),
            size_hint=(None, None)
        )
        self.gun = Gun(
            size=(50, 20),
            size_hint=(None, None)
        )

        # interfaz

        self.reader = KeyboardReader()
        self.player_move = PlayerMove()



        self.button = ButtonB()
        self.button_A = ButtonA()
        Window.bind(on_joy_axis=self.on_joy_axis)






    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def generate_game(self, level):
        self.reset(level)
        self.count_of_bulls = self.count_of_bulls + self.level * 2

        count_of_enemies = self.level * 3
        for j in range(count_of_enemies):
            rangos_x = [(0, 50), (Window.width - 50, Window.width)]
            inicio, fin = random.choice(rangos_x)
            position_x = random.randint(inicio, fin)

            rangos_y = [(0, 55), (Window.height - 55, Window.height)]
            inicio, fin = random.choice(rangos_y)
            position_y = random.randint(inicio, fin)

            enemy = Mummy(
                size=(self.size_enemy, self.size_enemy),
                pos=(position_x, position_y),
                size_hint=(None, None)
            )
            enemy.set_new_velocity(0.05 * self.level)
            self.enemies.append(enemy)
            self.add_widget(enemy)
        self.add_widget(self.button)
        self.add_widget(self.gun)
        self.add_widget(self.player)
        self.add_widget(self.button_A)

        self.update_event = Clock.schedule_interval(self.update, 1 / 120)
        self.bullet_gen_event = Clock.schedule_interval(self.generate_bullet, 3)

    def reset_game(self, level_number):
        self.clear_widgets()
        self.level = level_number
        self.level_passed = False

        # Limpiar listas
        self.enemies.clear()
        self.bullets.clear()
        self.bullets_to_agregate.clear()

        # Reiniciar jugador
        self.player.pos = (self.pos_initial_x, self.pos_initial_y)
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.count_of_bulls = self.count_of_bulls + self.level * 2

    def stop_game(self):
        if self.update_event:
            self.update_event.cancel()
        if self.bullet_gen_event:
            self.bullet_gen_event.cancel()

    def update(self, dt):
        self.gun.move(self.player.x, self.player.y)
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

        if self.bullets_to_agregate:
            for bullet in self.bullets_to_agregate:
                if bullet.collide_widget(self.player):
                    self.count_of_bulls += 1
                    self.bullets_to_agregate.remove(bullet)
                    self.remove_widget(bullet)

        if len(self.enemies) == 0:
            Clock.schedule_once(self.pass_level, 0)
            self.level_passed = True

        self.player_move.move(self.player)



    def pass_level(self, *args):
        self.stop()
        next_level = self.level + 1

        screen_new_level = self.manager.get_screen("ScreenNewLevel")
        screen_new_level.set_level(next_level)
        self.manager.current = "ScreenNewLevel"

    def go_to_finish(self, *args):
        self.stop()
        self.manager.current = "finish"

    def shoot_bullet(self):
        if self.count_of_bulls > 0:
            bullet = Bullet(pos=(self.gun.center_x - 7, self.gun.center_y - 7), size=(15, 15), size_hint=(None, None))
            self.count_of_bulls -= 1
            self.bullets.append(bullet)
            self.add_widget(bullet)

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


    def readDevice(self):

        pass





    def reset(self, level_number):
        self.clear_widgets()
        self.level = level_number
        self.level_passed = False

        self.enemies.clear()
        self.bullets.clear()
        self.bullets_to_agregate.clear()

        self.player.pos = (self.pos_initial_x, self.pos_initial_y)
        self.player.velocity_x = 0
        self.player.velocity_y = 0

    def stop(self):
        if self.update_event:
            self.update_event.cancel()
        if self.bullet_gen_event:
            self.bullet_gen_event.cancel()

    def is_caught(self, enemies: Mummy):
        return enemies.collide_widget(self.player)

    def on_touch_down(self, touch):
        condition_x_shoot =  800 <= touch.x <= 880
        condition_y_shoot = 150 <= touch.y <= 230

        if condition_x_shoot and condition_y_shoot:
            self.shoot_bullet()


    def on_touch_up(self, touch):
        self.player.velocity_y = 0
        self.player.velocity_x = 0

    def on_joy_axis(self, window, stickid, axisid, value):
        if axisid == 0:
            if value > 0:
                self.player.velocity_x = 5
            if value == 0:
                self.player.velocity_x = 0
            if value < 0:
                self.player.velocity_x = -5
        elif axisid == 1:
            if value > -1:
                self.player.velocity_y = -5
            if value == -1:
                self.player.velocity_y = 0
            if value < -1:
                self.player.velocity_y = +5
        else:
            self.player.velocity_x = 0
            self.player.velocity_y = 0


    def on_button_down(self, window, stickid, buttonid):
        if buttonid == 0:
            self.shoot_bullet()