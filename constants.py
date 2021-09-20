import pygame
import random
import os
from platform import system

NET = True
STOP_COLOR = False

POINTS_PER_FIGURE = 5

FIELD_WIDTH = 15
FIELD_HEIGHT = 20

SCORE_TABLE_HEIGHT = 100

FRAME_THICKNESS = 10
POINT_SIZE = 25

TIME_PER_MOVE = 400
ACCELERATE_TIME_PER_MOVE = 100

POINTS_PER_STOP = 10
POINTS_PER_LINE = 100

WINDOW_WIDTH = FIELD_WIDTH * POINT_SIZE + 2 * FRAME_THICKNESS
WINDOW_HEIGHT = SCORE_TABLE_HEIGHT + FIELD_HEIGHT * POINT_SIZE + 2 * FRAME_THICKNESS

FONT_SIZE = 34
FONT = 'bb3273.ttf'

if system() == 'Windows':
    WAY = os.getenv('APPDATA') + r'\..\Local\Games\pent\record.json'
else:  # system() == 'Linux':
    WAY = r'~/record/record.json'
if not os.path.exists(os.path.dirname(WAY)):
    os.makedirs(os.path.dirname(WAY))


COLORS = {
    'RED': pygame.Color(255, 0, 0),
    'YELLOW': pygame.Color(255, 204, 51),
    'PINK': pygame.Color(153, 51, 153),
    'PURPLE': pygame.Color(102, 0, 102),
    'WHITE': pygame.Color(255, 255, 255),
    'BLACK': pygame.Color(0, 0, 0),
    'BLUE': pygame.Color(0, 0, 153),
    'GREEN': pygame.Color(51, 102, 0),
    'STOP_COLOR': pygame.Color(0, 0, 51),
}


def get_random_color(expectations):
    colors_keys = list(COLORS.keys())
    if isinstance(expectations, list):
        for expectation in expectations:
            colors_keys.remove(expectation)
    else:
        colors_keys.remove(expectations)
    return COLORS[random.choice(colors_keys)]
