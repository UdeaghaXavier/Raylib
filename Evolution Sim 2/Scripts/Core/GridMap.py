from Scripts.Global.var import *
from Scripts.Core.Camera import CustomCamera
from Scripts.Core.Entity import Entity, Food


class GridMap:
    def __init__(self, size: int, width: float):
        self.map_size = size
        self.spacing = GRID_SPACING
        self.grid_width = width
        self.map: list[list[Entity]] = self.new_map()

    def draw(self, camera: CustomCamera):
        self.draw_camera_view(camera)

    def update(self):
        pass

    def handle_input(self):
        pass

    def new_map(self):
        grid_map = []
        for _ in range(self.map_size):
            col = []
            for _ in range(self.map_size):
                col.append(None)
            grid_map.append(col)

        return grid_map

    def convert_pos_to_coord(self, pos):
        px, py = pos

        x = (px - self.spacing) / (self.grid_width + self.spacing)
        y = (py - self.spacing) / (self.grid_width + self.spacing)

        return x, y

    def convert_coord_to_pos(self, pos):
        x, y = pos
        px = (
            x * (self.grid_width + self.spacing) + self.spacing
        )  # Remove extra spacing adjustment
        py = y * (self.grid_width + self.spacing) + self.spacing

        return px, py

    def get_top_left_coord_to_center_obj(
        self, pos: tuple[int, int], size: float
    ) -> tuple[int, int]:
        hw = self.grid_width / 2  # Half width of the grid cell
        hs = size / 2  # Half width of the entity

        gx, gy = pos  # Top-left of Grid
        cx, cy = gx + hw, gy + hw  # Center of grid cell

        dx = cx - hs  # Centered top-left X
        dy = cy - hs  # Centered top-left Y

        return round(dx), round(dy)  # Ensure integers for Raylib

    def draw_grid_id(self, pos):
        x, y = pos
        px, py = self.convert_coord_to_pos(pos)

        font_size = 1
        text = f"{x}, {y}"

        x, y = self.get_top_left_coord_to_center_obj((px, py), font_size * len(text))
        draw_text(text, x, y, font_size, WHITE)

    def draw_entity(self, entity: Entity, pos: tuple[int, int]):
        px, py = self.convert_coord_to_pos(pos)  # Get top-left grid position
        w = round(entity.stats.size * self.grid_width)  # Entity size in pixels

        # Find the grid center
        x, y = self.get_top_left_coord_to_center_obj((px, py), w)

        draw_rectangle(x, y, w, w, entity.stats.col)

    def draw_food(self, food: Food, pos: tuple[int, int]):
        px, py = self.convert_coord_to_pos(pos)
        w = round(food.size * self.grid_width)

        cx, cy = int(px + w / 2), int(py + w / 2)
        draw_circle(cx, cy, w / 2, RED)

    def draw_camera_view(self, camera: CustomCamera):
        cam = camera.camera
        cam_size = camera.size
        offset = 0  # extra gap to hide the fact that sm things arent being drawn
        # get top left and top right of the cameras current view
        px, py = cam.target.x - offset, cam.target.y - offset

        x1, y1 = self.convert_pos_to_coord((px, py))
        x1, y1 = int(x1), int(y1)

        # get number of rows / cols this camera can currently view
        r = round((cam_size - self.spacing) / self.grid_width)

        for dy in range(r):
            y = y1 + dy
            y = int(clamp(y, 0, self.map_size - 1))
            for dx in range(r):
                x = x1 + dx
                x = int(clamp(x, 0, self.map_size - 1))
                grid = self.map[y][x]

                if grid:
                    if type(grid) == Entity:
                        self.draw_entity(grid, (x, y))
                    elif type(grid) == Food:
                        self.draw_food(grid, (x, y))
                else:
                    self.draw_grid_id((x, y))
