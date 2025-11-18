import random

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

        # NUEVO: Configurar texturas para los tiles
        self.tile_map.set_tile_texture(TileMap.TILE_WALL, 'src/tumba.png')
        self.tile_map.set_tile_texture(TileMap.TILE_FLOOR, 'src/hazard.png')
        self.tile_map.set_tile_texture(TileMap.TILE_HAZARD, 'src/hazard.png')

        # Diferentes mapas según el nivel
        if level == 1:
            self.tile_map.create_border_map(Window.width, Window.height, border_thickness=2)
        elif level == 2:
            self.tile_map.create_room_map(Window.width, Window.height)
        elif level >= 3:
            map_matrix = self._get_map_matrix_for_level(level)
            self.tile_map.create_from_matrix(map_matrix)

        # Agregar el mapa al juego
        self.add_widget(self.tile_map)
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
            max_attempts = 100
            attempt = 0
            valid_position_found = False

            while attempt < max_attempts and not valid_position_found:
                # Generar posición aleatoria en el área jugable
                # Evitar spawns muy cerca del jugador
                min_distance = 200
                max_distance = 450

                # Ángulo aleatorio
                angle = random.uniform(0, 2 * 3.14159)
                distance = random.uniform(min_distance, max_distance)

                # Calcular posición relativa al jugador
                pos_x = self.player.x + distance * random.choice([-1, 1])
                pos_y = self.player.y + distance * random.choice([-1, 1])

                # Asegurar que esté dentro de los límites del mapa
                map_width, map_height = self.tile_map.get_map_dimensions()
                pos_x = max(enemy.width, min(pos_x, map_width - enemy.width))
                pos_y = max(enemy.height, min(pos_y, map_height - enemy.height))

                # Verificar si la posición es válida (sin colisión con paredes)
                if not self.tile_map.check_collision(pos_x, pos_y, enemy.width, enemy.height):
                    enemy.pos = (pos_x, pos_y)
                    valid_position_found = True

                attempt += 1

            # Si no se encontró posición válida después de todos los intentos,
            # colocar cerca del spawn del jugador (que sabemos es válido)
            if not valid_position_found:
                spawn_x, spawn_y = self.tile_map.get_spawn_position()
                offset = 100
                enemy.pos = (spawn_x + offset, spawn_y + offset)

    def _get_random_valid_position_in_map(self):
        """
        Método auxiliar: obtiene una posición aleatoria válida en cualquier parte del mapa
        Útil para spawns más distribuidos
        """
        map_width, map_height = self.tile_map.get_map_dimensions()
        tile_size = self.tile_map.tile_size

        max_attempts = 200
        for _ in range(max_attempts):
            # Generar coordenadas aleatorias alineadas a la grilla de tiles
            col = random.randint(2, self.tile_map.cols - 3)
            row = random.randint(2, self.tile_map.rows - 3)

            pos_x = col * tile_size
            pos_y = row * tile_size

            # Verificar que sea una posición válida (no hay colisión)
            if not self.tile_map.check_collision(pos_x, pos_y, self.size_player, self.size_player):
                return pos_x, pos_y

        # Si falla, retornar spawn del jugador
        return self.tile_map.get_spawn_position()

    def _spawn_enemies_distributed(self):
        """
        Alternativa: distribuye enemigos por todo el mapa de forma más uniforme
        Reemplaza a _spawn_enemies_in_valid_positions si prefieres esta estrategia
        """
        for enemy in self.enemies:
            pos_x, pos_y = self._get_random_valid_position_in_map()
            enemy.pos = (pos_x, pos_y)

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
        # MEJORADO: Los enemigos se mueven con deslizamiento por paredes
        for enemy in self.enemies:
            # Calcular movimiento deseado SIN aplicarlo
            velocity_x, velocity_y = enemy.calculate_movement(self.player.x, self.player.y)

            # Aplicar movimiento con colisiones del mapa
            new_x, new_y = self.tile_map.get_valid_position(
                enemy.x, enemy.y,
                enemy.width, enemy.height,
                velocity_x, velocity_y
            )

            enemy.pos = (new_x, new_y)

        self._check_collisions()

        # El movimiento del jugador ahora considera el mapa
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
        if self.id is not None:
            repository = PostgresUserRepository()
            search = UserFinder(repository)
            fila = search.search_by_id(self.id)
            level_max = fila[0][3]
            if self.level > level_max:
                search.update(self.id, self.level)

        self.manager.current = "finish"

    def set_id(self, id: int | None):
        self.id = id