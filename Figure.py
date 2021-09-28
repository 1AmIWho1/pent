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

    def get_width(self):
        start = 0
        for j in range(constants.POINTS_PER_FIGURE):
            for i in range(constants.POINTS_PER_FIGURE):
                if self.shape[i][j]:
                    start = j
                    break
        end = 0
        for j in range(constants.POINTS_PER_FIGURE - 1, 0, -1):
            for i in range(constants.POINTS_PER_FIGURE - 1, 0, -1):
                if self.shape[i][j]:
                    end = j
                    break
        return abs(end - start) + 1

    def get_empty_left(self, column=0):
        for i in range(constants.POINTS_PER_FIGURE):
            if self.shape[i][column]:
                return column
        column += 1
        return self.get_empty_left(column)

    def get_empty_right(self, column=constants.POINTS_PER_FIGURE-1):
        for i in range(constants.POINTS_PER_FIGURE):
            if self.shape[i][column]:
                return column
        column -= 1
        return self.get_empty_right(column)

    def get_empty_top(self, line=0):
        for i in range(constants.POINTS_PER_FIGURE):
            if self.shape[line][i]:
                return line
        line += 1
        return self.get_empty_top(line)

    def get_empty_bottom(self, line=constants.POINTS_PER_FIGURE-1):
        for i in range(constants.POINTS_PER_FIGURE):
            if self.shape[line][i]:
                return line
        line -= 1
        return self.get_empty_bottom(line)

    def get_height(self):
        return constants.POINTS_PER_FIGURE - list(map(lambda x: list(x), self.shape))\
            .count([False for i in range(constants.POINTS_PER_FIGURE)])

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


if __name__ == '__main__':
    f = Figure()
    print(f.shape)
    print(f.get_empty_left())
