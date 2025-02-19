from Scripts.Core.Camera import CustomCamera
from Scripts.Core.GridMap import GridMap
from Scripts.Core.Entity_Manager import Entity_Manager
from Scripts.Global.var import *


class World:
    def __init__(self):
        self.map_scale = MAP_SCALE
        self.camera = CustomCamera(self.map_scale)
        self.grid_size = GRID_SZIE  # size of each grid in pixels
        # number of rows and cols
        self.map_size = round(SCREEN_SIZE[0] / self.grid_size) * self.map_scale
        self.grid_map = GridMap(self.map_size, self.grid_size)
        self.entities_manager = Entity_Manager(self.grid_map)
        self.game_update_delay = GAME_FRAMES_UPDATE_DELAY
        self.frame = 0

    def draw(self):
        begin_mode_2d(self.camera.camera)
        self.grid_map.draw(self.camera)
        end_mode_2d()

    def update(self):
        if self.frame % self.game_update_delay == 0:
            self.entities_manager.update()

        self.grid_map.update()
        self.camera.update()

        self.frame += 1

    def handle_input(self):
        self.grid_map.handle_input()
        self.camera.handle_input()
