from enemy_render import EnemyRenderer
from kivy.core.image import Image as CoreImage


class TankRenderer(EnemyRenderer):
    def __init__(self):
        self.texture_path = "src/premium asset pack/Premium Undead Animations/Death Knight/DeathKnight.png"

        super().__init__(
            texture_path=self.texture_path,
            sprite_w=16,
            sprite_h=16,
            display_size=70,
            total_frames=4
        )

