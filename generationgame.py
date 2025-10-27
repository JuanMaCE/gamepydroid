import random
from mummy import Mummy



class GenerationGame:
    def __init__(self, level, window_size):
        self.level = level
        self.window_size = window_size
        self.size_enemy = 100

    def generate_enemies(self):
        enemies = []
        count_of_enemies = self.level * 3

        for _ in range(count_of_enemies):
            position = self._generate_random_position()
            enemy = Mummy(
                size=(self.size_enemy, self.size_enemy),
                pos=position,
                size_hint=(None, None)
            )
            enemy.set_new_velocity(0.05 * self.level)
            enemies.append(enemy)

        return enemies

    def _generate_random_position(self):
        rangos_x = [(0, 50), (self.window_size[0] - 50, self.window_size[0])]
        inicio, fin = random.choice(rangos_x)
        position_x = random.randint(inicio, fin)

        rangos_y = [(0, 55), (self.window_size[1] - 55, self.window_size[1])]
        inicio, fin = random.choice(rangos_y)
        position_y = random.randint(inicio, fin)

        return (position_x, position_y)

    def calculate_initial_bullets(self, base_count):
        return base_count + self.level * 2