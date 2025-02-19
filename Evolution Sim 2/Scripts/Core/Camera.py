from Scripts.Global.var import *
from Scripts.Global.misc import Controls


class CustomCamera:
    def __init__(self, map_scale: int):
        self.map_scale = map_scale
        self.camera = Camera2D()
        self.scroll_direction = (0, 0)
        self.zoom_direction = 0
        self.zoom_inc = 0.2
        self.scroll_spd = 10
        self.size = 0

        self.init_camera()

    def init_camera(self):

        self.camera.offset = (0, 0)  # No offset
        self.camera.target = HALF_SCREEN_SZIE  # Camera shld focus at this point
        self.camera.rotation = 0
        self.camera.zoom = 2

    def draw(self):
        pass

    def clip_movement(self):
        sx, sy = SCREEN_SIZE[0] * self.map_scale, SCREEN_SIZE[0] * self.map_scale
        s = SCREEN_SIZE[0] / self.camera.zoom  # camera view size

        x1, y1 = self.camera.target.x, self.camera.target.y

        x1 = clamp(x1, -s / 4, sx - s / 2)
        y1 = clamp(y1, -s / 4, sy - s / 2)

        self.camera.target.x = x1
        self.camera.target.y = y1
        self.size = s

    def clip_zoom(self):
        z = self.camera.zoom
        min_zoom = 0.4
        max_zoom = 8

        z = clamp(z, min_zoom, max_zoom)

        self.camera.zoom = z

    def update_camera_properties(self):
        x, y = self.camera.target.x, self.camera.target.y
        z = self.camera.zoom
        dx, dy = self.scroll_direction
        dz = self.zoom_direction

        x += dx * self.scroll_spd * (self.camera.zoom**-1)
        y += dy * self.scroll_spd * (self.camera.zoom**-1)
        z += dz * self.zoom_inc

        self.camera.target.x = x
        self.camera.target.y = y
        self.camera.zoom = z

    def update(self):
        self.update_camera_properties()
        self.clip_movement()
        self.clip_zoom()

    def handle_scroll_controls(self):
        dx, dy = self.scroll_direction

        if is_key_pressed(Controls.up):
            dy = -1
        elif is_key_pressed(Controls.down):
            dy = 1

        if is_key_pressed(Controls.left):
            dx = -1
        elif is_key_pressed(Controls.right):
            dx = 1

        if is_key_released(Controls.up) or is_key_released(Controls.down):
            dy = 0
        if is_key_released(Controls.left) or is_key_released(Controls.right):
            dx = 0

        self.scroll_direction = dx, dy

    def handle_zoom_controls(self):
        z = self.zoom_direction

        if is_key_pressed(Controls.zoom_in):
            z = 1
        elif is_key_pressed(Controls.zoom_out):
            z = -1

        if is_key_released(Controls.zoom_in) or is_key_released(Controls.zoom_out):
            z = 0

        self.zoom_direction = z

    def handle_input(self):
        self.handle_scroll_controls()
        self.handle_zoom_controls()
