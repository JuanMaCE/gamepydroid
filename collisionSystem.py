class CollisionSystem:
    @staticmethod
    def check_bullet_enemy_collisions(bullets, enemies, remove_widget_callback):
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if bullet.collide_widget(enemy):
                    remove_widget_callback(enemy)
                    remove_widget_callback(bullet)
                    enemies_to_remove.append(enemy)
                    bullets_to_remove.append(bullet)
                    break

        return bullets_to_remove, enemies_to_remove

    @staticmethod
    def check_player_enemy_collision(player, enemies):
        for enemy in enemies:
            if player.collide_widget(enemy):
                return True
        return False

    @staticmethod
    def check_bullet_pickup_collisions(player, bullets_to_agregate, remove_widget_callback):
        collected_bullets = []

        for bullet in bullets_to_agregate:
            if bullet.collide_widget(player):
                remove_widget_callback(bullet)
                collected_bullets.append(bullet)

        return collected_bullets