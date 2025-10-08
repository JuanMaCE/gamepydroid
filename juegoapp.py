from kivy.app import App
from game import  Game




class JuegoApp(App):
    def build(self):
        return Game()