from kivy.clock import Clock

class CollisionSystem:
    @staticmethod
    def check_bullet_enemy_collisions(bullets, enemies):
        """
        Detecta colisiones entre bullets y enemigos.
        Devuelve listas de bullets y enemigos a eliminar,
        y aplica daño solo a enemigos con health.
        """
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if bullet.collide_widget(enemy):
                    # Solo los enemigos cambian de color
                    if hasattr(enemy, "logic") and hasattr(enemy.logic, "health"):
                        enemy.renderer.set_color((1, 0, 0, 1))  # rojo
                        Clock.schedule_once(
                            lambda dt, e=enemy: e.renderer.set_color((1, 1, 1, 1)), 0.2
                        )

                        enemy.logic.health -= 1
                        if enemy.logic.health <= 0:
                            enemies_to_remove.append(enemy)
                    else:
                        enemies_to_remove.append(enemy)

                    bullets_to_remove.append(bullet)
                    break  # Un bullet solo daña a un enemigo

        return bullets_to_remove, enemies_to_remove

    @staticmethod
    def check_player_enemy_collision(player, enemies):
        """
        Devuelve True si el jugador colisiona con algún enemigo.
        """
        for enemy in enemies:
            if player.collide_widget(enemy):
                return True
        return False

    @staticmethod
    def check_bullet_pickup_collisions(player, bullets_to_agregate):
        """
        Detecta bullets recogidas por el jugador.
        Devuelve lista de bullets a agregar al inventario.
        """
        collected_bullets = []

        for bullet in bullets_to_agregate:
            if bullet.collide_widget(player):
                collected_bullets.append(bullet)

        return collected_bullets
