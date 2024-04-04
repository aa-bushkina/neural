import pygame as py

py.font.init()

# Окно приложения
FPS = 30
WIN_WIDTH = 900
WIN_HEIGHT = 900
STARTING_POS = (WIN_WIDTH / 2, WIN_HEIGHT - 100)

# Цвета
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Дорога
ROAD_DBG = False
MAX_ANGLE = 1
MAX_DEVIATION = 300
SPACING = 200
NUM_POINTS = 15
SAFE_SPACE = SPACING + 50
ROAD_WIDTH = 200

# Машина
MAX_VEL = 10
IMG_NAMES = ["bike_gray.png", "bike_white.png", "car_blue.png", "car_brown.png", "car_fam.png", "car_gliter.png",
             "car_orange.png", "car_purple.png", "car_red.png", "car_sport.png"]
ACTIVATION_TRESHOLD = 0.5
FRICTION = -0.1
ACC_STRENGTH = 0.2
BRAKE_STRENGTH = 1
TURN_VEL: int = 2
MAX_VEL_REDUCTION = 1
SENSOR_DISTANCE = 200
CAR_DBG = False

# Управление машиной
ACC = 0
BRAKE = 1
TURN_LEFT = 2
TURN_RIGHT = 3

# Настройки отображение генома
NODE_FONT = py.font.SysFont("comicsans", 15)
NODE_RADIUS = 20
NODE_SPACING = 5
LAYER_SPACING = 100
CONNECTION_WIDTH = 1
INPUT = 0
MIDDLE = 1
OUTPUT = 2
