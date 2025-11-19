# enemy_factory.py
from enemy_widget import EnemyWidget
from mummy_logic import MummyLogic
from mummy_render import MummyRenderer
from summer_mummy_logic import SummonerMummyLogic
from summoner_mummy_renderer import SummonerMummyRenderer
from tank_enemy_logic import TankLogic
from tank_render import TankRenderer
import random


class EnemyFactory:

    AVAILABLE_ENEMIES = [
        "mummy",
        "summoner",
        "tank"
    ]

    @staticmethod
    def create_enemy_random(pos):
        """Devuelve un enemigo random de la lista AVAILABLE_ENEMIES."""
        choice = random.choice(EnemyFactory.AVAILABLE_ENEMIES)
        if choice == "mummy":
            return EnemyFactory.create_mummy(pos)
        elif choice == "summoner":
            return EnemyFactory.create_summoner_mummy(pos)
        elif choice == "tank":
            return EnemyFactory.create_tank(pos)

    @staticmethod
    def create_mummy(pos):
        return EnemyWidget(
            logic=MummyLogic(),
            renderer=MummyRenderer(),
            pos=pos,
            size_hint=(None, None)
        )

    @staticmethod
    def create_summoner_mummy(pos):
        return EnemyWidget(
            logic=SummonerMummyLogic(),
            renderer=SummonerMummyRenderer(),
            pos=pos,
            size_hint=(None, None)
        )

    @staticmethod
    def create_tank(pos):
        return EnemyWidget(
            logic=TankLogic(),
            renderer=TankRenderer(),
            pos=pos,
            size_hint=(None, None)
        )