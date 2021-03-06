import constants
import json
import random


class Figure:

    def __init__(self):
        self.shape = [[False for i in range(constants.POINTS_PER_FIGURE)] for i in range(constants.POINTS_PER_FIGURE)]
        self.color = constants.get_random_color(['WHITE', 'STOP_COLOR', 'BLACK'])
        self.shapes = []
        self.load_shapes()
        self.get_shape()

    def load_shapes(self):
        with open('static/figures.bin', 'rb') as figures_bin:
            figures_tmp = list(map(bool, list(figures_bin.read())))
            for i in range(constants.FIGURES_COUNT):
                self.shapes.append([])
                for j in range(constants.POINTS_PER_FIGURE):
                    self.shapes[i].append(list(
                        figures_tmp[i * (constants.POINTS_PER_FIGURE ** 2) + j * constants.POINTS_PER_FIGURE:
                                    i * (constants.POINTS_PER_FIGURE ** 2) + (j + 1) * constants.POINTS_PER_FIGURE]))

    def get_shape(self):
        self.shape = random.choice(self.shapes)
        for i in range(random.randint(0, 3)):
            self.rotate(True)

    def get_shape_json(self):
        with open('static/figures.json', 'r') as figures_json:
            figures = json.load(figures_json)
            self.shape = random.choice(figures)
        for i in range(random.randint(0, 3)):
            self.rotate(True)

    def get_empty_figure(self):
        self.shape = [[False for i in range(constants.POINTS_PER_FIGURE)] for i in range(constants.POINTS_PER_FIGURE)]
        return self

    def get_width(self):
        start = 0
        for j in range(constants.POINTS_PER_FIGURE):
            for i in range(constants.POINTS_PER_FIGURE):
                if self.shape[i][j]:
                    start = j
                    break
        end = 0
        for j in range(constants.POINTS_PER_FIGURE - 1, -1, -1):
            for i in range(constants.POINTS_PER_FIGURE - 1, -1, -1):
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
        try:
            for i in range(constants.POINTS_PER_FIGURE):
                if self.shape[i][column]:
                    return column
            column -= 1
        except IndexError:
            return constants.POINTS_PER_FIGURE
        return self.get_empty_right(column)

    def get_empty_top(self, line=0):
        try:
            for i in range(constants.POINTS_PER_FIGURE):
                if self.shape[line][i]:
                    return line
            line += 1
        except IndexError:
            return constants.POINTS_PER_FIGURE
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

    def rotate(self, direction: bool):
        new_shape = [line[:] for line in self.shape]
        if direction:
            for i in range(constants.POINTS_PER_FIGURE):
                for j in range(constants.POINTS_PER_FIGURE):
                    new_shape[j][i] = self.shape[i][constants.POINTS_PER_FIGURE - j - 1]
        else:
            for i in range(constants.POINTS_PER_FIGURE):
                for j in range(constants.POINTS_PER_FIGURE):
                    new_shape[i][constants.POINTS_PER_FIGURE - j - 1] = self.shape[j][i]
        self.shape = new_shape


if __name__ == '__main__':
    f = Figure()
    print(f.shape)
    print(f.get_empty_left())
