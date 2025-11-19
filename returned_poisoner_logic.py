# returned_poisoner_logic.py
from enemy_logic import EnemyLogic

class ReturnedPoisonerLogic(EnemyLogic):
    def __init__(self):
        super().__init__(velocity=1)
        self.sprint_velocity = 3  # velocidad durante el sprint
        self.sprint_cooldown = 3.0  # cada 3 segundos
        self.timer = 0

    def update(self, dt, enemy_widget, spawn_callback, player_x, player_y):
        # Actualizar timer
        self.timer += dt

        # Determinar velocidad actual
        current_velocity = self.sprint_velocity if self.timer >= self.sprint_cooldown else self.velocity

        # Movimiento hacia el jugador
        vx, vy = self.calculate_movement(enemy_widget.x, enemy_widget.y, player_x, player_y)

        # NO usar índices, vx y vy son floats
        enemy_widget.x += vx * dt * 60 * current_velocity
        enemy_widget.y += vy * dt * 60 * current_velocity

        # Reset del sprint
        if self.timer >= self.sprint_cooldown:
            self.timer = 0
