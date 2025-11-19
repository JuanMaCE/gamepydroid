# hulking_brute_renderer.py
from enemy_render import EnemyRenderer

class HulkingBruteRenderer(EnemyRenderer):


    def __init__(self):
        super().__init__(
            texture_path="src/premium asset pack/Premium Undead Animations/Hulking Brute/HulkingBrute.png",
            sprite_w=16,       # ancho de cada frame en px
            sprite_h=16,       # alto de cada frame en px
            display_size=70,  # más grande que los otros enemigos
            total_frames=4
        )
