from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.animation import Animation

Window.clearcolor = (0.1, 0, 0, 1)


class RankingItem(BoxLayout):
    def __init__(self, position, name, score, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 70
        self.padding = [10, 5]
        self.spacing = 15

        # Color según posición
        colors = {
            1: (1, 0.84, 0, 1),  # Oro
            2: (0.75, 0.75, 0.75, 1),  # Plata
            3: (0.8, 0.5, 0.2, 1)  # Bronce
        }
        bg_color = colors.get(position, (0.2, 0, 0, 1))

        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

        self.bind(pos=self.update_rect, size=self.update_rect)

        # Medalla para top 3
        medal_text = ""
        if position == 1:
            medal_text = "🥇"
        elif position == 2:
            medal_text = "🥈"
        elif position == 3:
            medal_text = "🥉"

        # Posición
        pos_label = Label(
            text=f"{medal_text}\n#{position}" if medal_text else f"#{position}",
            size_hint_x=0.2,
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1)
        )

        # Nombre
        name_label = Label(
            text=name,
            size_hint_x=0.5,
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))

        # Puntuación
        score_label = Label(
            text=f"{score:,} pts",
            size_hint_x=0.3,
            font_size='22sp',
            bold=True,
            color=(0.3, 1, 0.5, 1),
            halign='right',
            valign='middle'
        )
        score_label.bind(size=score_label.setter('text_size'))

        self.add_widget(pos_label)
        self.add_widget(name_label)
        self.add_widget(score_label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RankingApp(App):
    def build(self):
        # Datos de ejemplo
        self.ranking_data = [
            {"name": "AlexGamer", "score": 15420},
            {"name": "MariaPro", "score": 14850},
            {"name": "CarlosX", "score": 13990},
            {"name": "LunaStrike", "score": 12760},
            {"name": "DiegoMaster", "score": 11540},
            {"name": "SofiaElite", "score": 10890},
            {"name": "JuanSpeed", "score": 9870},
            {"name": "AnaVictory", "score": 8920},
        ]

        # Ordenar por puntuación
        self.ranking_data.sort(key=lambda x: x['score'], reverse=True)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Título con efecto
        title_box = BoxLayout(size_hint_y=0.15)
        with title_box.canvas.before:
            Color(0.15, 0, 0, 1)
            self.title_rect = RoundedRectangle(pos=title_box.pos, size=title_box.size, radius=[20])
        title_box.bind(pos=self.update_title_rect, size=self.update_title_rect)

        title = Label(
            text="🏆 RANKING TOP JUGADORES 🏆",
            font_size='32sp',
            bold=True,
            color=(1, 0.84, 0, 1)
        )
        title_box.add_widget(title)

        # ScrollView para el ranking
        scroll = ScrollView(size_hint=(1, 0.65))
        ranking_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=[10, 10]
        )
        ranking_layout.bind(minimum_height=ranking_layout.setter('height'))

        # Agregar items del ranking
        for i, player in enumerate(self.ranking_data, 1):
            item = RankingItem(i, player['name'], player['score'])
            ranking_layout.add_widget(item)

        scroll.add_widget(ranking_layout)

        # Panel para agregar nuevo jugador
        add_panel = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=10)

        self.name_input = TextInput(
            hint_text='Nombre del jugador',
            size_hint_x=0.4,
            multiline=False,
            font_size='16sp',
            background_color=(0.1, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0, 0, 1)
        )

        self.score_input = TextInput(
            hint_text='Puntuación',
            size_hint_x=0.3,
            multiline=False,
            input_filter='int',
            font_size='16sp',
            background_color=(0.1, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0, 0, 1)
        )

        add_button = Button(
            text='Agregar',
            size_hint_x=0.3,
            font_size='18sp',
            bold=True,
            background_color=(0.8, 0, 0, 1),
            background_normal=''
        )
        add_button.bind(on_press=self.add_player)

        add_panel.add_widget(self.name_input)
        add_panel.add_widget(self.score_input)
        add_panel.add_widget(add_button)

        # Nota informativa
        info = Label(
            text='Agrega nuevos jugadores al ranking',
            size_hint_y=0.08,
            font_size='14sp',
            italic=True,
            color=(0.7, 0.7, 0.8, 1)
        )

        main_layout.add_widget(title_box)
        main_layout.add_widget(scroll)
        main_layout.add_widget(add_panel)
        main_layout.add_widget(info)

        self.scroll = scroll
        self.ranking_layout = ranking_layout

        return main_layout

    def update_title_rect(self, instance, value):
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size

    def add_player(self, instance):
        name = self.name_input.text.strip()
        score_text = self.score_input.text.strip()

        if name and score_text:
            try:
                score = int(score_text)
                self.ranking_data.append({"name": name, "score": score})
                self.ranking_data.sort(key=lambda x: x['score'], reverse=True)

                # Limpiar inputs
                self.name_input.text = ''
                self.score_input.text = ''

                # Actualizar ranking
                self.ranking_layout.clear_widgets()
                for i, player in enumerate(self.ranking_data, 1):
                    item = RankingItem(i, player['name'], player['score'])
                    self.ranking_layout.add_widget(item)

            except ValueError:
                pass


if __name__ == '__main__':
    RankingApp().run()