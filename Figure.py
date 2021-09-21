import constants
import json
import random
import numpy as np


class Figure:

    def __init__(self):
        self.shape = [[False for i in range(constants.POINTS_PER_FIGURE)] for i in range(constants.POINTS_PER_FIGURE)]
        self.color = constants.get_random_color(['WHITE', 'STOP_COLOR', 'BLACK'])
        self.get_shape()

    def get_shape(self):
        with open('figures.json', 'r') as figures_json:
            figures = json.load(figures_json)
            self.shape = random.choice(figures)
        for i in range(random.randint(0, 3)):
            self.rotate(True)

    def check_point(self, x, y):
        try:
            if self.shape[y][x]:
                return True
        except IndexError:
            pass
        return False

    def is_near_point_filled(self, x, y):
        if self.check_point(x + 1, y):
            return True
        if self.check_point(x - 1, y):
            return True
        if self.check_point(x, y + 1):
            return True
        if self.check_point(x, y - 1):
            return True
        return False

    def rotate(self, direction: bool):
        if direction:
            self.shape = np.rot90(self.shape)
        else:
            for i in range(3):
                self.shape = np.rot90(self.shape)
