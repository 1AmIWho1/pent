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
            self.rotate(1)

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

    def get_random_shape(self):  # need to be fixed
        self.shape[POINTS_PER_FIGURE // 2][POINTS_PER_FIGURE // 2] = True
        for i in range(POINTS_PER_FIGURE - 1):
            while True:
                tmp_x = random.randint(0, POINTS_PER_FIGURE - 1)
                tmp_y = random.randint(0, POINTS_PER_FIGURE - 1)
                if not self.shape[tmp_y][tmp_x] and self.is_near_point_filled(tmp_x, tmp_y):
                    self.shape[tmp_y][tmp_x] = True
                    break
        while True:
            try:
                self.shape.remove([False for i in range(POINTS_PER_FIGURE)])
            except ValueError:
                break
        point = 0
        while point < len(self.shape[0]):
            tmp = 0
            for line in range(len(self.shape)):
                if not self.shape[line][point]:
                    tmp += 1
            if tmp == len(self.shape):
                for line in range(len(self.shape)):
                    self.shape[line].pop(point)
                point -= 1
            point += 1

    def rotate(self, direction: bool):
        if direction:
            self.shape = np.rot90(self.shape)
        else:
            for i in range(3):
                self.shape = np.rot90(self.shape)
