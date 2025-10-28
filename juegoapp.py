from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from mainmenu import MainMenu
from finish import Finish
from game import  Game
from screennewlevel import ScreenNewLevel



class JuegoApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(ScreenNewLevel(name="ScreenNewLevel"))
        sm.add_widget(Game(name='game'))
        sm.add_widget(Finish(name='finish'))
        sm.add_widget(MainMenu(name='menu'))

        #sm.get_screen("ScreenNewLevel").set_level(1)
        #sm.current = "ScreenNewLevel"
        sm.current = "menu"
        return sm



