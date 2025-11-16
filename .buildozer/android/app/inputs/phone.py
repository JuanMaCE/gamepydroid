from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from inputs.inputdevice import InputDevice


def _inside(touch, rect):
    x, y = touch.pos
    rx, ry = rect.pos
    rw, rh = rect.size
    return rx <= x <= rx + rw and ry <= y <= ry + rh


class Phone(InputDevice):
    def __init__(self):
        super().__init__()
        self.data = {
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.parent = None
        self.btn_left = None
        self.btn_right = None
        self.btn_up = None
        self.btn_down = None
        self.btn_shoot = None

        self.pressed_buttons = set()

    def set_parent_widget(self, parent_widget):
        self.parent = parent_widget
        self._draw_buttons()
        self._bind_events()

    def _draw_buttons(self):
        self.parent.canvas.clear()

        def create_3d_button(pos, size):
            x, y = pos
            w, h = size
            with self.parent.canvas:
                # Base gris oscuro
                Color(0.4, 0.4, 0.4, 0.9)
                rect_base = Rectangle(pos=pos, size=size)
                # Bordes claros (arriba/izquierda)
                Color(0.8, 0.8, 0.8, 0.9)
                Rectangle(pos=pos, size=(w, 3))  # borde superior
                Rectangle(pos=pos, size=(3, h))  # borde izquierdo
                # Bordes oscuros (abajo/derecha)
                Color(0.2, 0.2, 0.2, 0.9)
                Rectangle(pos=(x, y + h - 3), size=(w, 3))  # borde inferior
                Rectangle(pos=(x + w - 3, y), size=(3, h))  # borde derecho
            return rect_base

        def create_simple_button(pos, size):
            with self.parent.canvas:
                Color(0.4, 0.4, 0.4, 0.9)
                rect = Rectangle(pos=pos, size=size)
            return rect

        btn_w, btn_h = (80, 80)
        spacing = 10

        base_x = 150
        base_y = 70

        vertical_gap = 20

        self.btn_down = create_3d_button((base_x, base_y), (btn_w, btn_h))
        self.btn_up = create_3d_button((base_x, base_y + btn_h + vertical_gap), (btn_w, btn_h))
        self.btn_left = create_3d_button((base_x - btn_w - spacing, base_y), (btn_w, btn_h))
        self.btn_right = create_3d_button((base_x + btn_w + spacing, base_y), (btn_w, btn_h))

        shoot_size = (100, 100)
        shoot_x = self.parent.width - shoot_size[0] - 40

        self.btn_shoot = create_simple_button((shoot_x - 50, 150), shoot_size)

        self._draw_arrows()

        self.parent.bind(size=self._update_buttons)

    def _draw_arrows(self):
        with self.parent.canvas:
            Color(1, 1, 1, 0.9)

            dpad_half = 40
            left_center = (self.btn_left.pos[0] + dpad_half, self.btn_left.pos[1] + dpad_half)
            right_center = (self.btn_right.pos[0] + dpad_half, self.btn_right.pos[1] + dpad_half)
            up_center = (self.btn_up.pos[0] + dpad_half, self.btn_up.pos[1] + dpad_half)
            down_center = (self.btn_down.pos[0] + dpad_half, self.btn_down.pos[1] + dpad_half)

            Line(points=[
                left_center[0] + 15, left_center[1],  # Punta
                left_center[0] - 10, left_center[1] - 10,  # Esquina inferior
                left_center[0] - 10, left_center[1] + 10  # Esquina superior
            ], width=2, close=True)

            Line(points=[
                right_center[0] - 15, right_center[1],  # Punta
                right_center[0] + 10, right_center[1] - 10,
                right_center[0] + 10, right_center[1] + 10
            ], width=2, close=True)

            Line(points=[
                up_center[0], up_center[1] + 15,  # Punta
                              up_center[0] - 10, up_center[1] - 10,
                              up_center[0] + 10, up_center[1] - 10
            ], width=2, close=True)

            Line(points=[
                down_center[0], down_center[1] - 15,  # Punta
                                down_center[0] - 10, down_center[1] + 10,
                                down_center[0] + 10, down_center[1] + 10
            ], width=2, close=True)



    def _update_buttons(self, *args):
        if self.parent and self.btn_shoot:
            width, height = self.parent.size

            shoot_x = width - 120
            self.btn_shoot.pos = (shoot_x, 40)

            self.parent.canvas.after.clear()
            self._draw_arrows()

    def _bind_events(self):
        self.parent.bind(on_touch_down=self._on_touch_down)
        self.parent.bind(on_touch_up=self._on_touch_up)

    def _on_touch_down(self, widget, touch):
        if _inside(touch, self.btn_left):
            self.data["x"] = -5
            self.pressed_buttons.add("left")
            return True
        elif _inside(touch, self.btn_right):
            self.data["x"] = 5
            self.pressed_buttons.add("right")
            return True
        elif _inside(touch, self.btn_up):
            self.data["y"] = 5
            self.pressed_buttons.add("up")
            return True
        elif _inside(touch, self.btn_down):
            self.data["y"] = -5
            self.pressed_buttons.add("down")
            return True
        elif _inside(touch, self.btn_shoot):
            self.data["z"] = 1
            self.pressed_buttons.add("shoot")
            print("shoot pressed")
            return True
        return False

    def _on_touch_up(self, widget, touch):
        if _inside(touch, self.btn_left) and "left" in self.pressed_buttons:
            self.data["x"] = 0
            self.pressed_buttons.discard("left")
            return True
        elif _inside(touch, self.btn_right) and "right" in self.pressed_buttons:
            self.data["x"] = 0
            self.pressed_buttons.discard("right")
            return True
        elif _inside(touch, self.btn_up) and "up" in self.pressed_buttons:
            self.data["y"] = 0
            self.pressed_buttons.discard("up")
            return True
        elif _inside(touch, self.btn_down) and "down" in self.pressed_buttons:
            self.data["y"] = 0
            self.pressed_buttons.discard("down")
            return True
        elif _inside(touch, self.btn_shoot) and "shoot" in self.pressed_buttons:
            self.data["z"] = 0
            self.pressed_buttons.discard("shoot")
            print("shoot released")
            return True
        return False

    def readData(self):
        print(f"Phone data: {self.data}")
        return self.data.copy()