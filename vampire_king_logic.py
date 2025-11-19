from enemy_logic import EnemyLogic

class VampireKingLogic(EnemyLogic):
    """
    Lógica del Rey Vampiro: no sigue al jugador.
    Puede realizar ataques periódicos u otras acciones.
    """

    def __init__(self):
        super().__init__(velocity=0)  # no se mueve
        self.attack_cooldown = 5.0
        self.timer = 0

    def update(self, dt, enemy_widget, *args):
        self.timer += dt
        if self.timer >= self.attack_cooldown:
            self.timer = 0
            # Ataque visual a pantalla completa
            enemy_widget.renderer.play_fullscreen_attack()
