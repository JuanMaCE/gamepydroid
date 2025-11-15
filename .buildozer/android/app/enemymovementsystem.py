class EnemyMovementSystem:
    @staticmethod
    def move_enemies(enemies, player_x, player_y):
        for enemy in enemies:
            enemy.follow_player(player_x, player_y)