from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from users.postgress_user_repository import PostgresUserRepository
from users.userfinder import UserFinder

# Importa tus componentes personalizados
from doombutton import DoomButton
from doomlabel import DoomLabel

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


class RankingScreen(Screen):
    def __init__(self, **kwargs):
        super(RankingScreen, self).__init__(**kwargs)

        # Fondo con imagen
        with self.canvas.before:
            self.bg = Rectangle(
                source='src/ranking_bg.png',
                size=self.size,
                pos=self.pos
            )
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Obtener datos de PostgreSQL
        self.repository = PostgresUserRepository()
        rows = self.repository.search_top()

        # Convertir las tuplas de PostgreSQL a diccionarios
        # Estructura de la tabla: id, name, password, level
        self.ranking_data = []
        for row in rows:
            self.ranking_data.append({
                'name': row[1],  # name está en posición 1
                'score': row[3]  # level está en posición 3
            })

        # Si no hay datos, usar datos de ejemplo
        if not self.ranking_data:
            self.ranking_data = [
                {"name": "Sin jugadores", "score": 0}
            ]

        # Ordenar por puntuación (aunque ya viene ordenado de la BD)
        self.ranking_data.sort(key=lambda x: x['score'], reverse=True)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Título con efecto usando DoomLabel
        title_box = BoxLayout(size_hint_y=0.15)
        with title_box.canvas.before:
            Color(0.15, 0, 0, 1)
            self.title_rect = RoundedRectangle(pos=title_box.pos, size=title_box.size, radius=[20])
        title_box.bind(pos=self.update_title_rect, size=self.update_title_rect)

        title = DoomLabel(
            text=" RANKING TOP JUGADORES ",
            font_size='32sp'
        )
        title_box.add_widget(title)

        # ScrollView para el ranking
        scroll = ScrollView(size_hint=(1, 0.75))
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

        # Botón para volver
        btn_back = DoomButton(
            text="Volver al Menú",
            size_hint_y=0.1,
            on_release=lambda btn: self.manager.go_to_main_menu(None)
        )

        main_layout.add_widget(title_box)
        main_layout.add_widget(scroll)
        main_layout.add_widget(btn_back)

        self.ranking_layout = ranking_layout

        # Agregar el layout a la pantalla
        self.add_widget(main_layout)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def update_title_rect(self, instance, value):
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size