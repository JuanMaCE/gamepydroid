# returned_poisoner_renderer.py
from enemy_render import EnemyRenderer

class ReturnedPoisonerRenderer(EnemyRenderer):
    """
    Renderer para el Returned Poisoner.
    Usa el spritesheet:
    src/premium asset pack/Premium Undead Animations/Returned Poisoner/ReturnedPosioner.png
    """

    def __init__(self):
        super().__init__(
            texture_path="src/premium asset pack/Premium Undead Animations/Returned Poisoner/ReturnedPoisoner.png",
            sprite_w=16,      # ancho de cada frame en px
            sprite_h=16,      # alto de cada frame en px
            display_size=64,  # tamaño normal
            total_frames=4
        )

    # Opcional: efecto visual al sprint
    def play_sprint_effect(self):
        if not hasattr(self, "rect"):
            return
        orig_size = self.rect.size
        try:
            self.rect.size = (orig_size[0] * 1.1, orig_size[1] * 1.1)
        except Exception:
            pass
