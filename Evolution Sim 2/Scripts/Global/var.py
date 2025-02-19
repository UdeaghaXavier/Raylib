from pyray import *
import random


SEED = 2007  # For entity and food generation
random.seed(SEED)

SCREEN_SIZE = 800, 800
HALF_SCREEN_SZIE = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
FPS = 60
TITLE = "Evolution Sim"

MAP_SCALE = 5
GRID_SZIE = 32
GRID_SPACING = 4

GAME_FRAMES_UPDATE_DELAY = 15  # 4 times a sec
MAX_HUNGER = 10
FOOD_VALUE = 10
STARTING_ENTITIES = 100

MIN_FOOD_PERCENATGE = 0.25
MAX_FOOD_PERCENTAGE = 1.0
