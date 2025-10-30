from kivy.uix.screenmanager import ScreenManager, FadeTransition
from mainmenu import MainMenu
from finish import Finish
from game import Game
from screennewlevel import ScreenNewLevel
from login.loginmenu import LoginMenu
from login.loginscreen import LoginScreen
from login.registerscreen import RegisterScreen
from rankingscreen import RankingScreen

class ScreenController(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(transition=FadeTransition(duration=1), **kwargs)
        self.add_widget(ScreenNewLevel(name="ScreenNewLevel"))
        self.add_widget(Game(name='game'))
        self.add_widget(Finish(name='finish'))
        self.add_widget(MainMenu(name='menu'))
        self.add_widget(LoginMenu(name="login"))
        self.add_widget(LoginScreen(name="login_screen"))
        self.add_widget(RegisterScreen(name="register_screen"))
        self.add_widget(RankingScreen(name='ranking'))

        self.current = "login"

    def go_to_login(self):
        self.current = "login"

    def go_to_register(self):
        self.current = "register_screen"

    def go_to_main_menu(self, id: int | None):
        screenNewLevel = self.get_screen("menu")
        screenNewLevel.set_new_id(id)
        self.current = 'menu'


    def go_to_login_screen(self):
        self.current = "login_screen"

    def go_to_play(self, id: int | None):
        screenNewLevel = self.get_screen("ScreenNewLevel")
        screenNewLevel.set_level(1)
        screenNewLevel.set_id(id)
        self.current = 'ScreenNewLevel'

    def go_to_ranking(self):
        self.current = 'ranking'