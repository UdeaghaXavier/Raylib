from Scripts.Global.var import *
from Scripts.Core.World import World


class Main:
    def __init__(self):
        init_window(SCREEN_SIZE[0], SCREEN_SIZE[1], TITLE)
        set_target_fps(FPS)

        self.world = World()

    def draw(self):
        begin_drawing()
        clear_background(SKYBLUE)
        self.world.draw()
        end_drawing()

    def update(self):
        self.handle_input()
        self.world.update()

    def handle_input(self):
        self.world.handle_input()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()


if __name__ == "__main__":
    Main().run()
    close_window()
