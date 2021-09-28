import constants


class Field:  # model

    def __init__(self, width, height, stop_color):
        self.stop_color = stop_color
        self.width = width
        self.height = height
        self.field = [[False for i in range(self.width)] for i in range(self.height)]

    def add_figure(self, figure, x, y):
        if self.stop_color:
            figure.color = constants.COLORS['STOP_COLOR']  # возможно есть смысл задавать STOP_COLOR непосредственно в self.stop_color
        for line in range(y, y + len(figure.shape)):
            for point in range(len(figure.shape[0])):
                if figure.shape[line - y][point]:
                    try:
                        self.field[line][x + point] = figure.color
                    except IndexError:
                        pass

    def delete_line(self, line):
        for item in range(line, 0, -1):
            self.field[item] = self.field[item - 1]
        self.field[0] = [False for i in range(self.width)]
