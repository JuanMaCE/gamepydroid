from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from finish import Finish
from game import  Game
from loading_screen import LoadingScreen
from screennewlevel import ScreenNewLevel



class JuegoApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(Game(1, name='game'))
        sm.add_widget(Finish(name='finish'))
        level_1 = ScreenNewLevel(1, name="screenNewLevel")
        sm.add_widget(level_1)
        sm.current = 'loading'
        return sm

