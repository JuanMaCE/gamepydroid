# tank_logic.py
from enemy_logic import EnemyLogic

class TankLogic(EnemyLogic):
    """Enemigo tanque: más lento y resistente."""
    def __init__(self):
        super().__init__(velocity=0.3)  # más lento que la momia
        self.health = 3  # aguanta 3 disparos
