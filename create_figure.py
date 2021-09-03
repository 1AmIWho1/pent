import json
import random
import numpy as np
from constants import get_random_color
from constants import POINTS_PER_FIGURE as PPF


class Figure:

    def __init__(self):
        self.shape = [[False for i in range(PPF)] for i in range(PPF)]
        self.color = get_random_color('WHITE')
        self.get_random_shape()

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

    def get_random_shape(self):
        self.shape[PPF // 2][PPF // 2] = True
        for i in range(PPF - 1):
            while True:
                tmp_x = random.randint(0, PPF - 1)
                tmp_y = random.randint(0, PPF - 1)
                if not self.shape[tmp_y][tmp_x] and self.is_near_point_filled(tmp_x, tmp_y):
                    self.shape[tmp_y][tmp_x] = True
                    break
        while True:
            try:
                self.shape.remove([False for i in range(PPF)])
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

    def rotate(self, direction):
        if direction == 1:
            self.shape = np.rot90(self.shape)
        else:
            for i in range(3):
                self.shape = np.rot90(self.shape)
        self.shape = self.shape.tolist()


def main():
    figures = []
    with open('figures.json', 'r') as figures_json:
        figures = json.load(figures_json)
        for i in range(1000):
            f = Figure()
            if f.shape not in figures:
                f.rotate(1)
                if f.shape not in figures:
                    f.rotate(1)
                    if f.shape not in figures:
                        f.rotate(1)
                        if f.shape not in figures:
                            figures.append(f.shape)
    with open('figures.json', 'w') as figures_json:
        json.dump(figures, figures_json)
    print(len(figures))


def test():
    a = [[1, 2, 3]]
    a.extend([[5, 6, 7]])
    c = a[:]
    a = np.rot90(a)
    a = np.rot90(a)
    a = np.rot90(a)
    a = np.rot90(a)
    a = a.tolist()
    print(type(a))
    print(a)
    print(c)


if __name__ == '__main__':
    main()

