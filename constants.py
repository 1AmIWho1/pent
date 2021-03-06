import pygame
import random
import os
from platform import system

if system() == 'Windows':
    WAY_RECORD = os.getenv('APPDATA') + r'\..\Local\Games\pent\record.json'
    WAY_SETTINGS = os.getenv('APPDATA') + r'\..\Local\Games\pent\settings.json'
else:
    WAY_RECORD = r'/record/record.json'
    WAY_SETTINGS = r'/record/settings.json'
if not os.path.exists(os.path.dirname(WAY_RECORD)):
    os.makedirs(os.path.dirname(WAY_RECORD))

GRID = True
STOP_COLOR = False

FIGURES_COUNT = 18

POINTS_PER_FIGURE = 5

FIELD_WIDTH = 15
FIELD_HEIGHT = 20

SCORE_TABLE_HEIGHT = 100
SCORE_TABLE_WIDTH = 250

FRAME_THICKNESS = 10
POINT_SIZE = 25

TIME_PER_MOVE = 100
TIME_PER_FALL = 400
ACCELERATE_TIME_PER_MOVE = 50

POINTS_PER_STOP = 10

WINDOW_WIDTH = FIELD_WIDTH * POINT_SIZE + 2 * FRAME_THICKNESS + SCORE_TABLE_WIDTH
WINDOW_HEIGHT = FIELD_HEIGHT * POINT_SIZE + 2 * FRAME_THICKNESS

FONT_SIZE = 34
FONT = 'static/bb3273.ttf'
ICON = 'static/pent.png'

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
