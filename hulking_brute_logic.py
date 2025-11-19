# hulking_brute_logic.py
from enemy_logic import EnemyLogic

class HulkingBruteLogic(EnemyLogic):
    def __init__(self):
        # Velocidad más alta que la momia invocadora
        super().__init__(velocity=1)

    def update(self, dt, enemy_widget, spawn_callback, player_x, player_y):
        # Movimiento hacia el jugador
        vx, vy = self.calculate_movement(enemy_widget.x, enemy_widget.y,
                                         player_x, player_y)
        enemy_widget.x += vx * dt * 60
        enemy_widget.y += vy * dt * 60
        # Podrías agregar un ataque especial aquí si quieres
