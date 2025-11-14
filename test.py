from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window


class Tile:
    """Representa un tile individual del mapa"""

    def __init__(self, x, y, width, height, tile_type, texture=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile_type = tile_type  # 'solid', 'empty', 'hazard', etc.
        self.texture = texture
        self.rect = None  # Referencia al Rectangle de Kivy
        self.color_instruction = None  # Referencia al Color

    def is_solid(self):
        return self.tile_type in ['solid', 'wall']

    def get_bounds(self):
        """Retorna los límites del tile para colisiones"""
        return {
            'left': self.x,
            'right': self.x + self.width,
            'top': self.y + self.height,
            'bottom': self.y
        }

    def update_position(self, x, y, width, height):
        """Actualiza la posición y tamaño del tile"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if self.rect:
            self.rect.pos = (x, y)
            self.rect.size = (width, height)


class TileMap(Widget):
    """Sistema completo de mapa con tiles y colisiones"""

    # Tipos de tiles predefinidos
    TILE_EMPTY = 0
    TILE_WALL = 1
    TILE_FLOOR = 2
    TILE_HAZARD = 3

    # Colores por defecto para cada tipo
    TILE_COLORS = {
        TILE_EMPTY: (0, 0, 0, 0),  # Transparente
        TILE_WALL: (0.3, 0.3, 0.3, 1),  # Gris oscuro
        TILE_FLOOR: (0.6, 0.6, 0.6, 0.3),  # Gris claro semi-transparente
        TILE_HAZARD: (0.8, 0.2, 0.2, 0.7)  # Rojo
    }

    def __init__(self, tile_size=50, **kwargs):
        super().__init__(**kwargs)
        self.base_tile_size = tile_size  # Tamaño base de referencia
        self.tile_size = tile_size
        self.tiles = []
        self.map_data = []
        self.cols = 0
        self.rows = 0
        self.base_window_size = (Window.width, Window.height)

        # Vincular eventos de redimensionamiento
        Window.bind(size=self._on_window_resize)
        self.bind(size=self._on_widget_resize, pos=self._on_widget_resize)

    def _on_window_resize(self, instance, value):
        """Callback cuando la ventana cambia de tamaño"""
        if len(self.map_data) > 0:
            self._recalculate_and_redraw()

    def _on_widget_resize(self, instance, value):
        """Callback cuando el widget cambia de tamaño o posición"""
        if len(self.map_data) > 0:
            self._recalculate_and_redraw()

    def _recalculate_and_redraw(self):
        """Recalcula el tamaño de los tiles y redibuja el mapa"""
        if not self.map_data:
            return

        # Calcular nuevo tamaño de tile basado en el tamaño de la ventana
        # y el número de columnas/filas originales
        scale_x = Window.width / self.base_window_size[0]
        scale_y = Window.height / self.base_window_size[1]
        scale = min(scale_x, scale_y)  # Mantener proporción

        self.tile_size = int(self.base_tile_size * scale)

        # Redibujar el mapa con el nuevo tamaño
        self._redraw_map()

    def _redraw_map(self):
        """Redibuja el mapa completo con el tamaño actual"""
        self.canvas.clear()

        with self.canvas:
            for row_idx, row in enumerate(self.tiles):
                for col_idx, tile in enumerate(row):
                    x = col_idx * self.tile_size
                    y = (self.rows - row_idx - 1) * self.tile_size

                    # Actualizar posición del tile
                    tile.update_position(x, y, self.tile_size, self.tile_size)

                    # Redibujar si no es vacío
                    tile_type = self.map_data[row_idx][col_idx]
                    if tile_type != self.TILE_EMPTY:
                        color = self.TILE_COLORS.get(tile_type, (1, 1, 1, 1))
                        tile.color_instruction = Color(*color)
                        tile.rect = Rectangle(
                            pos=(tile.x, tile.y),
                            size=(tile.width, tile.height)
                        )

    def create_from_matrix(self, matrix):
        """
        Crea el mapa desde una matriz
        0 = vacío, 1 = pared/sólido, 2 = piso, 3 = peligro

        Dim matriz(,) As Integer = {

        Ejemplo:  11 x
        """
        matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.clear_map()
        self.map_data = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0

        # Guardar tamaño base de ventana
        self.base_window_size = (Window.width, Window.height)

        with self.canvas:
            for row_idx, row in enumerate(matrix):
                tile_row = []
                for col_idx, tile_type in enumerate(row):
                    x = col_idx * self.tile_size
                    y = (self.rows - row_idx - 1) * self.tile_size  # Invertir Y

                    tile = Tile(
                        x, y,
                        self.tile_size, self.tile_size,
                        self._get_tile_type_name(tile_type)
                    )

                    # Solo dibujar tiles visibles (no vacíos)
                    if tile_type != self.TILE_EMPTY:
                        color = self.TILE_COLORS.get(tile_type, (1, 1, 1, 1))
                        tile.color_instruction = Color(*color)
                        tile.rect = Rectangle(
                            pos=(tile.x, tile.y),
                            size=(tile.width, tile.height)
                        )

                    tile_row.append(tile)
                self.tiles.append(tile_row)

    def _get_tile_type_name(self, tile_type):
        """Convierte el número de tipo a nombre"""
        type_map = {
            self.TILE_EMPTY: 'empty',
            self.TILE_WALL: 'solid',
            self.TILE_FLOOR: 'floor',
            self.TILE_HAZARD: 'hazard'
        }
        return type_map.get(tile_type, 'empty')

    def create_border_map(self, width, height, border_thickness=1):
        """Crea un mapa rectangular con bordes sólidos"""
        cols = width // self.tile_size
        rows = height // self.tile_size

        matrix = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                # Bordes
                if (row < border_thickness or row >= rows - border_thickness or
                        col < border_thickness or col >= cols - border_thickness):
                    row_data.append(self.TILE_WALL)
                else:
                    row_data.append(self.TILE_EMPTY)
            matrix.append(row_data)

        self.create_from_matrix(matrix)

    def create_room_map(self, width, height):
        """Crea un mapa tipo habitación con paredes y algunos obstáculos"""
        cols = width // self.tile_size
        rows = height // self.tile_size

        matrix = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                # Bordes externos
                if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                    row_data.append(self.TILE_WALL)
                # Obstáculos internos (ejemplo)
                elif (row == rows // 2 and col > cols // 4 and col < 3 * cols // 4):
                    row_data.append(self.TILE_WALL)
                else:
                    row_data.append(self.TILE_EMPTY)
            matrix.append(row_data)

        self.create_from_matrix(matrix)

    def check_collision(self, x, y, width, height):
        """
        Verifica si un rectángulo colisiona con tiles sólidos
        Retorna True si hay colisión
        """
        # Calcular qué tiles podría estar tocando
        start_col = max(0, int(x // self.tile_size))
        end_col = min(self.cols - 1, int((x + width) // self.tile_size))
        start_row = max(0, int(y // self.tile_size))
        end_row = min(self.rows - 1, int((y + height) // self.tile_size))

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                    continue
                tile = self.tiles[self.rows - row - 1][col]  # Invertir Y
                if tile.is_solid():
                    if self._rectangles_intersect(
                            x, y, width, height,
                            tile.x, tile.y, tile.width, tile.height
                    ):
                        return True
        return False

    def get_valid_position(self, x, y, width, height, velocity_x, velocity_y):
        """
        Retorna una posición válida ajustada para evitar colisiones
        Usa sliding para movimiento suave contra paredes
        """
        new_x = x + velocity_x
        new_y = y + velocity_y

        # Verificar movimiento en X
        if not self.check_collision(new_x, y, width, height):
            x = new_x
        else:
            # Ajustar a la pared más cercana
            x = self._adjust_to_wall_x(x, y, width, height, velocity_x)

        # Verificar movimiento en Y
        if not self.check_collision(x, new_y, width, height):
            y = new_y
        else:
            # Ajustar a la pared más cercana
            y = self._adjust_to_wall_y(x, y, width, height, velocity_y)

        return x, y

    def _adjust_to_wall_x(self, x, y, width, height, velocity_x):
        """Ajusta la posición X para que quede pegada a la pared"""
        if self.tile_size == 0:
            return x
        col = int((x + width if velocity_x > 0 else x) // self.tile_size)
        if velocity_x > 0:
            return col * self.tile_size - width - 1
        else:
            return (col + 1) * self.tile_size + 1

    def _adjust_to_wall_y(self, x, y, width, height, velocity_y):
        """Ajusta la posición Y para que quede pegada a la pared"""
        if self.tile_size == 0:
            return y
        row = int((y + height if velocity_y > 0 else y) // self.tile_size)
        if velocity_y > 0:
            return row * self.tile_size - height - 1
        else:
            return (row + 1) * self.tile_size + 1

    def _rectangles_intersect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        """Verifica si dos rectángulos se intersectan"""
        return not (x1 + w1 < x2 or x2 + w2 < x1 or
                    y1 + h1 < y2 or y2 + h2 < y1)

    def get_tile_at_position(self, x, y):
        """Retorna el tile en una posición específica"""
        if self.tile_size == 0:
            return None
        col = int(x // self.tile_size)
        row = int(y // self.tile_size)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.tiles[self.rows - row - 1][col]
        return None

    def get_spawn_position(self):
        """Retorna una posición válida de spawn (centro del mapa aproximadamente)"""
        center_x = (self.cols * self.tile_size) // 2
        center_y = (self.rows * self.tile_size) // 2
        return center_x, center_y

    def get_map_dimensions(self):
        """Retorna las dimensiones actuales del mapa en píxeles"""
        return self.cols * self.tile_size, self.rows * self.tile_size

    def scale_position(self, old_x, old_y, old_window_size):
        """Escala una posición desde un tamaño de ventana anterior al actual"""
        scale_x = Window.width / old_window_size[0]
        scale_y = Window.height / old_window_size[1]
        return old_x * scale_x, old_y * scale_y

    def clear_map(self):
        """Limpia el mapa actual"""
        self.canvas.clear()
        self.tiles.clear()
        self.map_data.clear()
        self.cols = 0
        self.rows = 0


class MapCollisionHandler:
    """Manejador de colisiones específico para integrar con tu juego"""

    def __init__(self, tile_map):
        self.tile_map = tile_map

    def update_player_position(self, player, velocity_x, velocity_y):
        """
        Actualiza la posición del jugador considerando colisiones del mapa
        """
        new_x, new_y = self.tile_map.get_valid_position(
            player.x, player.y,
            player.width, player.height,
            velocity_x, velocity_y
        )

        player.x = new_x
        player.y = new_y

        return new_x, new_y

    def is_position_valid(self, x, y, width, height):
        """Verifica si una posición es válida (sin colisiones)"""
        return not self.tile_map.check_collision(x, y, width, height)