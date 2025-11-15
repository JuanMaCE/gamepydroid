import random
from mummy import Mummy


class GenerationGame:
    def __init__(self, level, window_size, tile_map=None):
        self.level = level
        self.window_size = window_size
        self.size_enemy = 100
        self.tile_map = tile_map  # NUEVO: Referencia al mapa

    def generate_enemies(self):
        enemies = []
        count_of_enemies = self.level * 3

        max_attempts = 10

        for _ in range(count_of_enemies):
            position = None

            for attempt in range(max_attempts):
                test_position = self._generate_random_position()

                # Si hay mapa, verificar que la posición sea válida
                if self.tile_map:
                    if not self.tile_map.check_collision(
                            test_position[0], test_position[1],
                            self.size_enemy, self.size_enemy
                    ):
                        position = test_position
                        break
                else:
                    # Sin mapa, usar la posición directamente
                    position = test_position
                    break

            # Si no se encontró posición válida, usar una posición central
            if position is None:
                if self.tile_map:
                    position = self.tile_map.get_spawn_position()
                else:
                    position = (self.window_size[0] // 2, self.window_size[1] // 2)

            enemy = Mummy(
                size=(self.size_enemy, self.size_enemy),
                pos=position,
                size_hint=(None, None)
            )
            enemy.set_new_velocity(0.05 * self.level)
            enemies.append(enemy)

        return enemies

    def _generate_random_position(self):
        """Genera una posición aleatoria en los bordes de la pantalla"""
        rangos_x = [(0, 50), (self.window_size[0] - 50, self.window_size[0])]
        inicio, fin = random.choice(rangos_x)
        position_x = random.randint(inicio, fin)

        rangos_y = [(0, 55), (self.window_size[1] - 55, self.window_size[1])]
        inicio, fin = random.choice(rangos_y)
        position_y = random.randint(inicio, fin)

        return (position_x, position_y)

    def calculate_initial_bullets(self, base_count):
        return base_count + self.level * 2

    def set_tile_map(self, tile_map):
        """Establece el mapa de tiles para validar posiciones"""
        self.tile_map = tile_map
