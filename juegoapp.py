from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from finish import Finish
from game import  Game
from loading_screen import LoadingScreen




class JuegoApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(Game(name='game'))
        sm.add_widget(Finish(name='finish'))
        sm.current = 'loading'
        return sm

