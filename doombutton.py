from kivy.uix.button import Button
from kivy.animation import Animation



class DoomButton(Button):
    def __init__(self ,**kwargs):
        super(DoomButton, self).__init__(**kwargs)
        self.font_size = '30sp'
        self.bold = True
        self.color = (1, 0.85, 0, 1)
        self.background_normal = ''
        self.background_color = (0.4, 0, 0, 1)
        self.size_hint = (1, 0.3)
        self.border = (8, 8, 8, 8)
        self.bind(on_enter=self.on_hover, on_leave=self.on_unhover)
        self.bind(on_press=self.on_press_button)

    def on_hover(self, *args):
        Animation(background_color=(0.8, 0.1, 0.1, 1), duration=0.2).start(self)

    def on_unhover(self, *args):
        Animation(background_color=(0.4, 0, 0, 1), duration=0.2).start(self)

    def on_press_button(self, instance):
        screen = self.parent
        while screen and not hasattr(screen, 'manager'):
            screen = screen.parent

        if screen and screen.manager:
            sm = screen.manager
            if sm.has_screen("ScreenNewLevel"):
                screenNewLevel = sm.get_screen("ScreenNewLevel")
                screenNewLevel.set_level(1)
                sm.current = "ScreenNewLevel"
            else:
                print("❌ Error: ScreenNewLevel no encontrado")
        else:
            print("❌ Error: No se pudo acceder al ScreenManager")