from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
import random


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

    # Colores por defecto para cada tipo (si no hay textura)
    TILE_COLORS = {
        TILE_EMPTY: (0, 0, 0, 0),  # Transparente
        TILE_WALL: (0.3, 0.3, 0.3, 1),  # Gris oscuro
        TILE_FLOOR: (0.6, 0.6, 0.6, 0.3),  # Gris claro semi-transparente
        TILE_HAZARD: (0.8, 0.2, 0.2, 0.7)  # Rojo
    }

    # Texturas/imágenes para cada tipo de tile
    TILE_TEXTURES = {
        TILE_EMPTY: None,
        TILE_WALL: None,  # Puedes asignar: 'ruta/a/wall.png'
        TILE_FLOOR: None,  # Puedes asignar: 'ruta/a/floor.png'
        TILE_HAZARD: None  # Puedes asignar: 'ruta/a/hazard.png'
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

    def set_tile_texture(self, tile_type, texture_path):
        """
        Permite configurar la textura para un tipo de tile específico

        Ejemplo:
        tile_map.set_tile_texture(TileMap.TILE_WALL, 'src/wall.png')
        tile_map.set_tile_texture(TileMap.TILE_FLOOR, 'src/floor.png')
        """
        self.TILE_TEXTURES[tile_type] = texture_path

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
                        # Usar textura si está disponible, sino usar color
                        texture = self.TILE_TEXTURES.get(tile_type)

                        if texture:
                            # Dibujar con textura
                            Color(1, 1, 1, 1)  # Color blanco para no alterar la textura
                            tile.rect = Rectangle(
                                pos=(tile.x, tile.y),
                                size=(tile.width, tile.height),
                                source=texture
                            )
                        else:
                            # Dibujar con color
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
        """
        matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1],
        ]
        matriz = modificar_matriz(matrix, bloques_individuales=15, cuadrados=10)

        self.clear_map()
        self.map_data = matriz
        self.rows = len(matriz)
        self.cols = len(matriz[0]) if self.rows > 0 else 0

        # Guardar tamaño base de ventana
        self.base_window_size = (Window.width, Window.height)

        with self.canvas:
            for row_idx, row in enumerate(matriz):
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
                        # Usar textura si está disponible, sino usar color
                        texture = self.TILE_TEXTURES.get(tile_type)

                        if texture:
                            # Dibujar con textura
                            Color(1, 1, 1, 1)  # Color blanco para no alterar la textura
                            tile.rect = Rectangle(
                                pos=(tile.x, tile.y),
                                size=(tile.width, tile.height),
                                source=texture
                            )
                        else:
                            # Dibujar con color
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
        Retorna una posición válida que simplemente detiene el movimiento en caso de colisión
        No ajusta bruscamente la posición, solo previene el movimiento
        Intenta movimiento por ejes separados para permitir deslizamiento
        """
        new_x = x
        new_y = y

        # Verificar movimiento en X
        if not self.check_collision(x + velocity_x, y, width, height):
            new_x = x + velocity_x

        # Verificar movimiento en Y
        if not self.check_collision(new_x, y + velocity_y, width, height):
            new_y = y + velocity_y

        return new_x, new_y

    def can_move_x(self, x, y, width, height, velocity_x):
        """Verifica si el movimiento en X es válido"""
        return not self.check_collision(x + velocity_x, y, width, height)

    def can_move_y(self, x, y, width, height, velocity_y):
        """Verifica si el movimiento en Y es válido"""
        return not self.check_collision(x, y + velocity_y, width, height)

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
        Simplemente detiene el movimiento si hay colisión, no ajusta bruscamente
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


def tiene_uno_adyacente(matriz, fila, col):
    """Verifica si hay un 1 adyacente (arriba, abajo, izquierda, derecha)"""
    filas = len(matriz)
    columnas = len(matriz[0])

    # Direcciones: arriba, abajo, izquierda, derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for df, dc in direcciones:
        nueva_fila, nueva_col = fila + df, col + dc

        # Verificar límites
        if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas:
            if matriz[nueva_fila][nueva_col] == 1:
                return True

    return False


def tiene_uno_en_radio(matriz, fila, col, radio=1):
    """
    Verifica si hay un 1 en el radio especificado alrededor de la posición
    radio=1 verifica las 8 casillas adyacentes
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    for df in range(-radio, radio + 1):
        for dc in range(-radio, radio + 1):
            if df == 0 and dc == 0:
                continue

            nueva_fila, nueva_col = fila + df, col + dc

            # Verificar límites
            if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas:
                if matriz[nueva_fila][nueva_col] == 1:
                    return True

    return False


def puede_colocar_cuadrado(matriz, fila, col):
    """
    Verifica si se puede colocar un cuadrado 2x2 en la posición
    y que no haya ningún 1 en las casillas adyacentes al cuadrado
    y que no esté en el centro de la matriz
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    # Verificar que el cuadrado cabe en la matriz
    if fila + 1 >= filas or col + 1 >= columnas:
        return False

    # Verificar que ninguna parte del cuadrado 2x2 esté en el centro
    if (es_centro_matriz(matriz, fila, col) or
            es_centro_matriz(matriz, fila, col + 1) or
            es_centro_matriz(matriz, fila + 1, col) or
            es_centro_matriz(matriz, fila + 1, col + 1)):
        return False

    # Verificar que las 4 posiciones estén libres
    if (matriz[fila][col] != 0 or matriz[fila][col + 1] != 0 or
            matriz[fila + 1][col] != 0 or matriz[fila + 1][col + 1] != 0):
        return False

    # Verificar que no haya ningún 1 alrededor del cuadrado 2x2
    # Necesitamos verificar un área de 4x4 centrada en el cuadrado
    for check_fila in range(fila - 1, fila + 3):
        for check_col in range(col - 1, col + 3):
            # Saltar las posiciones del cuadrado mismo
            if fila <= check_fila <= fila + 1 and col <= check_col <= col + 1:
                continue

            # Verificar límites
            if 0 <= check_fila < filas and 0 <= check_col < columnas:
                if matriz[check_fila][check_col] == 1:
                    return False

    return True


def colocar_cuadrado(matriz, fila, col):
    """Coloca un cuadrado 2x2 de 1s"""
    matriz[fila][col] = 1
    matriz[fila][col + 1] = 1
    matriz[fila + 1][col] = 1
    matriz[fila + 1][col + 1] = 1


def es_centro_matriz(matriz, fila, col, radio=2):
    """
    Verifica si la posición está en el centro de la matriz
    radio: define el área central a evitar
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    centro_fila = filas // 2
    centro_col = columnas // 2

    # Verificar si está dentro del radio del centro
    if abs(fila - centro_fila) <= radio and abs(col - centro_col) <= radio:
        return True

    return False


def colocar_bloque_individual(matriz):
    """
    Intenta colocar un bloque individual de 1
    que no esté pegado a ningún otro 1 y no esté en el centro
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    intentos = 0
    max_intentos = 1000

    while intentos < max_intentos:
        fila = random.randint(0, filas - 1)
        col = random.randint(0, columnas - 1)

        # Verificar que la posición esté vacía, no tenga 1s adyacentes y no esté en el centro
        if (matriz[fila][col] == 0 and
                not tiene_uno_adyacente(matriz, fila, col) and
                not es_centro_matriz(matriz, fila, col)):
            matriz[fila][col] = 1
            return True

        intentos += 1

    return False


def colocar_cuadrado_aleatorio(matriz):
    """Intenta colocar un cuadrado 2x2 de 1s sin 1s cerca"""
    filas = len(matriz)
    columnas = len(matriz[0])
    intentos = 0
    max_intentos = 1000

    while intentos < max_intentos:
        fila = random.randint(0, filas - 2)
        col = random.randint(0, columnas - 2)

        if puede_colocar_cuadrado(matriz, fila, col):
            colocar_cuadrado(matriz, fila, col)
            return True

        intentos += 1

    return False


def modificar_matriz(matriz, bloques_individuales=15, cuadrados=10):
    """
    Modifica una matriz existente agregando bloques individuales y cuadrados
    - Bloques individuales: no pueden estar pegados entre sí
    - Cuadrados 2x2: no pueden tener ningún 1 cerca
    """

    # Colocar cuadrados primero (son más restrictivos)
    cuadrados_colocados = 0
    for _ in range(cuadrados):
        if colocar_cuadrado_aleatorio(matriz):
            cuadrados_colocados += 1

    # Colocar bloques individuales (no pueden estar pegados)
    bloques_colocados = 0
    for _ in range(bloques_individuales):
        if colocar_bloque_individual(matriz):
            bloques_colocados += 1

    print(f"Cuadrados 2x2 colocados: {cuadrados_colocados}/{cuadrados}")
    print(f"Bloques individuales colocados: {bloques_colocados}/{bloques_individuales}")

    return matriz