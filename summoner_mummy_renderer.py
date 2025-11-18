# summoner_mummy_renderer.py
from enemy_render import EnemyRenderer

class SummonerMummyRenderer(EnemyRenderer):
    """
    Renderer para la momia invocadora (Summoner).
    Usa el spritesheet:
    src/premium asset pack/Premium Undead Animations/Blinded Acolyte/blindeadacolyte.png
    """

    def __init__(self):
        # Ajusta frame_w/frame_h/total_frames según tu spritesheet real
        # He puesto 16x16 y 6 frames como ejemplo; cámbialos si tu PNG difiere.
        super().__init__(
            texture_path="src/premium asset pack/Premium Undead Animations/Blinded Acolyte/BlindedAcolyte.png",
            sprite_w=16,
            sprite_h=16,
            display_size=64,   # invocador más grande
            total_frames=4
        )

    # Opcional: animación visual cuando invoca (pequeño pulso)
    def play_summon_effect(self):
        """
        Efecto visual sencillo: escala temporal del rect para dar sensación de casteo.
        Llamar desde la lógica justo antes de spawnear las momias.
        """
        if not hasattr(self, "rect"):
            return

        # Guardar tamaño original
        orig_size = self.rect.size

        # Escala rápida (sin usar Clock aquí, solo helper; lógicamente se puede
        # animar con Clock.schedule_interval desde la lógica si lo deseas)
        try:
            self.rect.size = (orig_size[0] * 1.15, orig_size[1] * 1.15)
        except Exception:
            pass
