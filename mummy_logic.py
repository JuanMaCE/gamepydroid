from enemy_logic import EnemyLogic

class MummyLogic(EnemyLogic):
    """Lógica específica de una momia."""
    def __init__(self):
        super().__init__(velocity=1.0)
