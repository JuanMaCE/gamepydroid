# enemy_factory.py
from enemy_widget import EnemyWidget
from mummy_logic import MummyLogic
from mummy_render import MummyRenderer
from summer_mummy_logic import SummonerMummyLogic
from summoner_mummy_renderer import SummonerMummyRenderer
from tank_enemy_logic import TankLogic
from tank_render import TankRenderer
from vampire_king_logic import VampireKingLogic
from vampire_king_renderer import VampireKingRenderer
from hulking_brute_logic import HulkingBruteLogic
from hulking_brute_renderer import HulkingBruteRenderer
from returned_poisoner_logic import ReturnedPoisonerLogic
from returned_poisoner_renderer import ReturnedPoisonerRenderer
import random


class EnemyFactory:

    AVAILABLE_ENEMIES = [
        "mummy",
        "summoner",
        "tank",
        "vampire_king",
        "hulking",
        "poisoner"
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
        elif choice == "vampire_king":
            return EnemyFactory.create_vampire_king(pos)
        elif choice == "hulking":
            return EnemyFactory.create_hulking(pos)
        elif choice == "poisoner":
            return EnemyFactory.create_poisoner(pos)

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

    @staticmethod
    def create_vampire_king(pos):
        return EnemyWidget(
            logic=VampireKingLogic(),
            renderer=VampireKingRenderer(),
            pos=pos,
            size_hint=(None, None)
        )

    @staticmethod
    def create_hulking(pos):
        return EnemyWidget(
            logic=HulkingBruteLogic(),
            renderer=HulkingBruteRenderer(),
            pos=pos,
            size_hint=(None, None)
        )

    @staticmethod
    def create_poisoner(pos):
        return EnemyWidget(
            logic=ReturnedPoisonerLogic(),
            renderer=ReturnedPoisonerRenderer(),
            pos=pos,
            size_hint=(None, None)
        )