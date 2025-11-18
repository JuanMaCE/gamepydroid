from kivy.uix.widget import Widget

class EnemyWidget(Widget):
    def __init__(self, logic, renderer, **kwargs):
        super().__init__(**kwargs)

        self.logic = logic
        self.renderer = renderer

        # Dibujar sprite
        self.renderer.attach(self)

    def calculate_movement(self, player_x, player_y):
        return self.logic.calculate_movement(self.x, self.y, player_x, player_y)

    def get_hitbox(self):
        hitbox_size = 1
        offset = (self.width - hitbox_size) / 2
        return (
            self.x + offset,
            self.y + offset,
            hitbox_size,
            hitbox_size
        )
