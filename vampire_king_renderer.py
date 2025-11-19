from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from enemy_render import EnemyRenderer
from kivy.core.window import Window
from kivy.uix.image import Image as UIXImage
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class VampireKingRenderer(EnemyRenderer):
    """
    Renderer para el Rey Vampiro.
    Permite mostrar un ataque visual a pantalla completa temporalmente.
    """

    def __init__(self):
        super().__init__(
            texture_path="src/premium asset pack/Premium Undead Animations/Bloodthirsty Count/BloodthirstyCount.png",
            sprite_w=16,
            sprite_h=16,
            display_size=64,
            total_frames=4
        )
        # Usaremos una lista para guardar todos los elementos del ataque (fondo + 5 murciélagos)
        self.attack_widgets = []

    def play_fullscreen_attack(self):
        # 1. Crear un fondo negro para tapar el juego ("que no se mire nada")
        bg_widget = Widget(size_hint=(1, 1))
        with bg_widget.canvas:
            Color(0, 0, 0, 1)  # Color Negro Opaco
            # Dibujamos un rectangulo del tamaño de la ventana
            Rectangle(pos=(0, 0), size=Window.size)

        Window.add_widget(bg_widget)
        self.attack_widgets.append(bg_widget)

        # 2. Configuración de los 5 murciélagos (4 esquinas + 1 centro)
        # Usamos size_hint para que sean proporcionales al tamaño de la ventana
        configs = [
            # Esquina Inferior Izquierda
            {'pos_hint': {'x': 0, 'y': 0}, 'size_hint': (0.5, 0.5)},
            # Esquina Inferior Derecha
            {'pos_hint': {'x': 0.5, 'y': 0}, 'size_hint': (0.5, 0.5)},
            # Esquina Superior Izquierda
            {'pos_hint': {'x': 0, 'y': 0.5}, 'size_hint': (0.5, 0.5)},
            # Esquina Superior Derecha
            {'pos_hint': {'x': 0.5, 'y': 0.5}, 'size_hint': (0.5, 0.5)},
            # Centro (Un poco más grande para imponer)
            {'pos_hint': {'center_x': 0.5, 'center_y': 0.5}, 'size_hint': (0.6, 0.6)}
        ]

        # 3. Crear y añadir los 5 murciélagos
        for config in configs:
            bat_img = UIXImage(
                source="src/premium asset pack/Premium Undead Animations/Bloodthirsty Count/bat.png",
                keep_ratio=True,  # Mantener proporción para que no se mire feo/estirado
                allow_stretch=True,  # Permitir que crezca
                size_hint=config['size_hint'],
                pos_hint=config['pos_hint']
            )
            Window.add_widget(bat_img)
            self.attack_widgets.append(bat_img)

        # 4. Programar limpieza (Ahora son 2 segundos)
        Clock.schedule_once(self.remove_attack_visual, 2)

    def remove_attack_visual(self, dt):
        # Eliminar todos los widgets creados (fondo + bats)
        for widget in self.attack_widgets:
            Window.remove_widget(widget)
        # Limpiar la lista
        self.attack_widgets = []