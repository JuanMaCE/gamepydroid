# enemy_logic.py
import math

class EnemyLogic:
    """Abstracción: cómo se comporta un enemigo."""
    def __init__(self, velocity):
        self.velocity = velocity

    def calculate_movement(self, enemy_x, enemy_y, player_x, player_y):
        """Devuelve un vector (vx, vy) sin aplicarlo."""
        angle = math.atan2(player_y - enemy_y, player_x - enemy_x)
        return math.cos(angle) * self.velocity, math.sin(angle) * self.velocity

    def update(self, dt, enemy_widget, spawn_callback, player_x, player_y):
        """Movimiento por defecto hacia el jugador."""
        vx, vy = self.calculate_movement(enemy_widget.x, enemy_widget.y,
                                         player_x, player_y)
        enemy_widget.x += vx * dt * 60
        enemy_widget.y += vy * dt * 60
