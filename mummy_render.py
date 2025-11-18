from enemy_render import EnemyRenderer

class MummyRenderer(EnemyRenderer):
    def __init__(self):
        super().__init__(
            texture_path="src/premium asset pack/Premium Undead Animations/Mummified Ritualist/MummifiedRitualist.png",
            sprite_w=16,
            sprite_h=16,
            display_size=48,
            total_frames=4
        )
