import constants


class Field:  # model

    def __init__(self):
        self.field = [[False for i in range(constants.FIELD_WIDTH)] for i in range(constants.FIELD_HEIGHT)]

    def add_figure(self, figure, x, y):
        if constants.STOP_COLOR:
            figure.color = constants.COLORS['STOP_COLOR']
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
        self.field[0] = [False for i in range(constants.FIELD_WIDTH)]
