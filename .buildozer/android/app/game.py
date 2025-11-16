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
from users.userfinder import UserFinder
from users.postgress_user_repository import PostgresUserRepository
from test import Tile, TileMap, MapCollisionHandler

class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemies = None
        self.id = None
        self.level = 1
        self.level_passed = False
        self.phone = PhoneReader

        # Sistemas
        self.generator = None
        self.collision_system = CollisionSystem()
        self.bullet_manager = BulletManager()

        # NUEVO: Sistema de mapa
        self.tile_map = None
        self.map_collision_handler = None

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

    def _setup_map(self, level):
        """Configura el mapa según el nivel"""
        # Remover mapa anterior si existe
        if self.tile_map:
            self.remove_widget(self.tile_map)

        # Crear nuevo mapa
        self.tile_map = TileMap(tile_size=50)

        # Diferentes mapas según el nivel
        if level == 1:
            # Mapa simple con bordes
            self.tile_map.create_border_map(Window.width, Window.height, border_thickness=2)

        elif level == 2:
            # Mapa con habitación y obstáculo central
            self.tile_map.create_room_map(Window.width, Window.height)

        elif level >= 3:
            # Mapas personalizados con matriz
            map_matrix = self._get_map_matrix_for_level(level)
            self.tile_map.create_from_matrix(map_matrix)

        # Agregar el mapa al juego (después del fondo, antes de las entidades)
        self.add_widget(self.tile_map)

        # Crear manejador de colisiones
        self.map_collision_handler = MapCollisionHandler(self.tile_map)

        # Colocar jugador en posición válida
        spawn_x, spawn_y = self.tile_map.get_spawn_position()
        self.player.pos = (spawn_x - self.size_player // 2, spawn_y - self.size_player // 2)

    def _get_map_matrix_for_level(self, level):
        """Retorna matrices de mapa personalizadas según el nivel"""
        # Calcular tamaño del mapa en tiles
        cols = Window.width // 50
        rows = Window.height // 50

        # Mapa laberinto simple
        if level == 3:
            # Crear matriz base
            matrix = [[0 for _ in range(cols)] for _ in range(rows)]

            # Bordes
            for i in range(cols):
                matrix[0][i] = 1
                matrix[rows - 1][i] = 1
            for i in range(rows):
                matrix[i][0] = 1
                matrix[i][cols - 1] = 1

            # Obstáculos internos en forma de laberinto
            mid_row = rows // 2
            for i in range(2, cols - 2):
                if i % 4 != 0:  # Dejar espacios
                    matrix[mid_row][i] = 1

            return matrix

        # Mapa con habitaciones
        elif level == 4:
            matrix = [[0 for _ in range(cols)] for _ in range(rows)]

            # Bordes externos
            for i in range(cols):
                matrix[0][i] = 1
                matrix[rows - 1][i] = 1
            for i in range(rows):
                matrix[i][0] = 1
                matrix[i][cols - 1] = 1

            # Crear "habitaciones" con paredes internas
            quarter_col = cols // 4
            quarter_row = rows // 4

            # Paredes horizontales
            for i in range(quarter_col, 3 * quarter_col):
                if i % 8 > 2:  # Dejar puertas
                    matrix[quarter_row][i] = 1
                    matrix[3 * quarter_row][i] = 1

            # Paredes verticales
            for i in range(quarter_row, 3 * quarter_row):
                if i % 8 > 2:  # Dejar puertas
                    matrix[i][quarter_col] = 1
                    matrix[i][3 * quarter_col] = 1

            return matrix

        # Por defecto, mapa con bordes
        else:
            matrix = [[0 for _ in range(cols)] for _ in range(rows)]
            for i in range(cols):
                matrix[0][i] = 1
                matrix[rows - 1][i] = 1
            for i in range(rows):
                matrix[i][0] = 1
                matrix[i][cols - 1] = 1
            return matrix

    def generate_game(self, level):
        self.reset(level)

        # NUEVO: Configurar mapa primero
        self._setup_map(level)

        # Usar el generador
        self.generator = GenerationGame(level, Window.size)
        self.enemies = self.generator.generate_enemies()

        # NUEVO: Asegurar que enemigos spawnen en posiciones válidas
        self._spawn_enemies_in_valid_positions()

        self.bullet_manager.add_bullets(self.generator.calculate_initial_bullets(5))

        # Agregar widgets
        self._add_game_widgets()

        # Iniciar eventos
        self._start_game_events()

    def _spawn_enemies_in_valid_positions(self):
        """Reposiciona enemigos para que no spawnen dentro de paredes"""
        for enemy in self.enemies:
            # Si el enemigo está en colisión, buscar posición cercana válida
            if self.tile_map.check_collision(enemy.x, enemy.y, enemy.width, enemy.height):
                # Intentar encontrar una posición válida cerca
                for offset_x in range(-100, 101, 50):
                    for offset_y in range(-100, 101, 50):
                        test_x = enemy.x + offset_x
                        test_y = enemy.y + offset_y
                        if not self.tile_map.check_collision(test_x, test_y, enemy.width, enemy.height):
                            enemy.pos = (test_x, test_y)
                            break

    def _add_game_widgets(self):
        # El mapa ya fue agregado en _setup_map
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
        # NUEVO: Los enemigos también deben respetar las paredes
        for enemy in self.enemies:
            # Guardar posición anterior
            old_x, old_y = enemy.x, enemy.y

            # Intentar seguir al jugador
            enemy.follow_player(self.player.x, self.player.y)

            # Verificar si la nueva posición colisiona
            if self.tile_map.check_collision(enemy.x, enemy.y, enemy.width, enemy.height):
                # Restaurar posición anterior
                enemy.pos = (old_x, old_y)

        self._check_collisions()

        # NUEVO: El movimiento del jugador ahora considera el mapa
        self._move_player_with_map_collision()

        self.bullet_manager.move_bullets(self.gun.angle)
        self._check_level_completion()

    def _move_player_with_map_collision(self):
        """Mueve al jugador considerando las colisiones del mapa"""
        # Guardar posición actual
        old_x, old_y = self.player.x, self.player.y

        # Dejar que PlayerMove calcule el movimiento normal
        self.player_move.move(self.player, self.gun, self.bullet_manager, self.add_widget)

        # Calcular velocidad resultante
        velocity_x = self.player.x - old_x
        velocity_y = self.player.y - old_y

        # Restaurar posición y aplicar movimiento con colisiones
        self.player.pos = (old_x, old_y)
        new_x, new_y = self.map_collision_handler.update_player_position(
            self.player, velocity_x, velocity_y
        )

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
        print(self.id)
        if self.id is not None:
            repository = PostgresUserRepository()
            search = UserFinder(repository)
            fila = search.search_by_id(self.id)
            level_max = fila[0][3]
            print(self.level, level_max)
            if self.level > level_max:
                search.update(self.id, self.level)

        self.manager.current = "finish"

    def set_id(self, id: int | None):
        self.id = id