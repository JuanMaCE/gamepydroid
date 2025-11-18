# summoner_mummy_logic.py
from enemy_logic import EnemyLogic

class SummonerMummyLogic(EnemyLogic):
    def __init__(self):
        super().__init__(velocity=0.6)
        self.summon_cooldown = 10.0
        self.timer = 0

    def update(self, dt, enemy_widget, spawn_callback, player_x, player_y):
        vx, vy = self.calculate_movement(enemy_widget.x, enemy_widget.y,
                                         player_x, player_y)
        enemy_widget.x += vx * dt * 60
        enemy_widget.y += vy * dt * 60

        self.timer += dt
        if self.timer >= self.summon_cooldown:
            self.timer = 0
            self.summon_mummies(enemy_widget, spawn_callback)

    def summon_mummies(self, enemy_widget, spawn_callback):
        positions = [
            (enemy_widget.x + 40, enemy_widget.y),
            (enemy_widget.x - 40, enemy_widget.y),
            (enemy_widget.x, enemy_widget.y + 40)
        ]
        for pos in positions:
            spawn_callback(pos)
