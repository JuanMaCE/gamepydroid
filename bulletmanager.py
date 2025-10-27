import random
from bullet import Bullet




class BulletManager:
    def __init__(self):
        self.bullets = []
        self.bullets_to_agregate = []
        self.bullet_count = 0

    def shoot_bullet(self, gun_pos, add_widget_callback):
        if self.bullet_count > 0:
            bullet = Bullet(
                pos=(gun_pos[0] - 7, gun_pos[1] - 7),
                size=(15, 15),
                size_hint=(None, None)
            )
            self.bullet_count -= 1
            self.bullets.append(bullet)
            add_widget_callback(bullet)
            return True
        return False

    def generate_random_bullet(self, window_size, add_widget_callback):
        size = 30
        x = random.randint(0, window_size[0] - size)
        y = random.randint(0, window_size[1] - size)

        new_bullet = Bullet(
            size=(size, size),
            pos=(x, y),
            size_hint=(None, None)
        )
        self.bullets_to_agregate.append(new_bullet)
        add_widget_callback(new_bullet)

    def move_bullets(self, gun_angle):
        for bullet in self.bullets:
            bullet.move(gun_angle)

    def add_bullets(self, count):
        self.bullet_count += count