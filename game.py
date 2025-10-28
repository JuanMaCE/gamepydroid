from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.window import Window
from bulletmanager import BulletManager
from collisionSystem import CollisionSystem
from generationgame import GenerationGame
from gun import Gun
from inputs.phonereader import PhoneReader
from player import Player
from inputs.player_move import PlayerMove

class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemies = None
        self.level = 1
        self.level_passed = False
        self.phone = PhoneReader
        # Sistemas
        self.generator = None
        self.collision_system = CollisionSystem()
        self.bullet_manager = BulletManager()

        # Eventos
        self.update_event = None
        self.bullet_gen_event = None

        # Configuración inicial
        self._setup_background()
        self._setup_entities()
        self._setup_input()

        self.player_move = PlayerMove()
        self.player_move.setup_phone_controls(self)

    def _setup_background(self):
        with self.canvas.before:
            self.bg = Rectangle(source='src/fondo.png', pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

    def _setup_entities(self):
        self.size_player = 70
        self.pos_initial_x = 400
        self.pos_initial_y = 225

        self.enemies = []

        self.player = Player(
            size=(self.size_player, self.size_player),
            size_hint=(None, None)
        )
        self.gun = Gun(
            size=(50, 20),
            size_hint=(None, None)
        )

    def _setup_input(self):
        self.player_move = PlayerMove()

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def generate_game(self, level):
        self.reset(level)

        # Usar el generador
        self.generator = GenerationGame(level, Window.size)
        self.enemies = self.generator.generate_enemies()
        self.bullet_manager.add_bullets(self.generator.calculate_initial_bullets(5))

        # Agregar widgets
        self._add_game_widgets()

        # Iniciar eventos
        self._start_game_events()

    def _add_game_widgets(self):
        self.add_widget(self.gun)
        self.add_widget(self.player)

        for enemy in self.enemies:
            self.add_widget(enemy)

    def _start_game_events(self):
        self.update_event = Clock.schedule_interval(self.update, 1 / 120)
        self.bullet_gen_event = Clock.schedule_interval(self._generate_bullet, 4)

    def _generate_bullet(self, dt):
        self.bullet_manager.generate_random_bullet(Window.size, self.add_widget)

    def update(self, dt):

        for enemy in self.enemies:
            enemy.follow_player(self.player.x, self.player.y)

        self._check_collisions()
        self.player_move.move(self.player, self.gun, self.bullet_manager, self.add_widget)
        self.bullet_manager.move_bullets(self.gun.angle)
        self._check_level_completion()

    def _check_collisions(self):
        bullets_to_remove, enemies_to_remove = self.collision_system.check_bullet_enemy_collisions(
            self.bullet_manager.bullets, self.enemies, self.remove_widget
        )

        for bullet in bullets_to_remove:
            self.bullet_manager.bullets.remove(bullet)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        if self.collision_system.check_player_enemy_collision(self.player, self.enemies):
            self._handle_player_death()

        collected_bullets = self.collision_system.check_bullet_pickup_collisions(
            self.player, self.bullet_manager.bullets_to_agregate, self.remove_widget
        )

        for bullet in collected_bullets:
            self.bullet_manager.bullets_to_agregate.remove(bullet)
            self.bullet_manager.add_bullets(1)

    def _handle_player_death(self):
        self.remove_widget(self.player)
        self.remove_widget(self.gun)
        Clock.schedule_once(self.go_to_finish, 0.1)

    def _check_level_completion(self):
        if len(self.enemies) == 0 and not self.level_passed:
            self.level_passed = True
            Clock.schedule_once(self.pass_level, 0)


    def reset_game(self, level_number):
        self.reset(level_number)

    def reset(self, level_number):
        self.clear_widgets()
        self.level = level_number
        self.level_passed = False
        self.enemies.clear()
        self.bullet_manager.bullets.clear()
        self.bullet_manager.bullets_to_agregate.clear()

        self.player.pos = (self.pos_initial_x, self.pos_initial_y)
        self.player.velocity_x = 0
        self.player.velocity_y = 0

    def stop_game(self):
        self.stop()

    def stop(self):
        if self.update_event:
            self.update_event.cancel()
        if self.bullet_gen_event:
            self.bullet_gen_event.cancel()

    def pass_level(self, *args):
        self.stop()
        next_level = self.level + 1

        screen_new_level = self.manager.get_screen("ScreenNewLevel")
        screen_new_level.set_level(next_level)
        self.manager.current = "ScreenNewLevel"

    def go_to_finish(self, *args):
        self.stop()
        self.manager.current = "finish"