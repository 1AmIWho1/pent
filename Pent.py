from Figure import Figure
from Field import Field
from Score import Score
import constants


class Pent:  # controller

    def __init__(self, field: Field):
        self.last_time = 0
        self.field = field
        self.time_per_move = constants.TIME_PER_MOVE
        self.score_inf = Score()
        self.accelerate_figure(False)
        self.figure = Figure()
        self.figure_x = (constants.FIELD_WIDTH - len(self.figure.shape[0])) // 2  # левая точка фигуры
        self.figure_y = 0  # верхняя точка фигуры

    def add_new_figure(self):  # добавляет новую фигуру сверху посередине
        self.accelerate_figure(False)
        self.figure = Figure()
        self.figure_x = (constants.FIELD_WIDTH - len(self.figure.shape[0])) // 2
        self.figure_y = 0

    def stop_figure(self):  # останавливает фигуру и записывает ее в поле
        self.field.add_figure(self.figure, self.figure_x, self.figure_y)
        self.score_inf.update(constants.POINTS_PER_STOP)

    def move_figure(self, direction):  # движение фигуры влево/вправо
        self.figure_x += direction
        if self.check_collision_right() or self.check_collision_left() or self.check_collision_down():
            self.figure_x -= direction

    def rotate_figure(self, direction: bool):  # вращение фигуры по/против часовой стрелке
        self.figure.rotate(direction)
        if self.check_collision_left() or self.check_collision_right() or self.check_collision_down():
            self.figure.rotate(not direction)

    def accelerate_figure(self, acc):  # ускорение фигуры
        if acc:
            self.time_per_move = constants.ACCELERATE_TIME_PER_MOVE
        else:
            self.time_per_move = constants.TIME_PER_MOVE

    def drop_figure(self):  # мгновенное падение фигуры
        while not self.check_collision_down():
            self.figure_y += 1
        self.stop_figure()
        self.add_new_figure()

    def fall_figure(self, time):  # нормальное падение фигуры
        collision = self.check_collision_down()
        if not collision and time - self.last_time >= self.time_per_move:
            self.figure_y += 1
            self.last_time = time
        elif collision:
            self.stop_figure()
            self.add_new_figure()

    def check_collision_left(self):  # проверяет, не наезжает ли одна движущаяся фигура на что-либо слева
        if 0 > self.figure_x:
            return True
        try:
            line = self.figure_y
            while line < self.figure_y + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):
                    if self.figure.shape[line - self.figure_y][point] and self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_right(self):    # проверяет, не наезжает ли одна движущаяся фигура на что-либо справа
        if self.figure_x + len(self.figure.shape[0]) > constants.FIELD_WIDTH:
            return True
        try:
            line = self.figure_y
            while line < self.figure_y + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):
                    if self.figure.shape[line - self.figure_y][point] and self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_down(self):
        if self.figure_y + len(self.figure.shape) > constants.FIELD_HEIGHT:
            return True
        try:
            line = self.figure_y + 1
            while line < self.figure_y + 1 + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):  # len(self.figure.shape[0]) - ширина фигуры
                    if self.figure.shape[line - (self.figure_y + 1)][point] and self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_and_stop(self):
        line = 0
        while line < constants.FIELD_HEIGHT:
            try:
                self.field.field[line].index(False)
            except ValueError:
                self.score_inf.update(constants.POINTS_PER_LINE)
                self.field.delete_line(line)
                line -= 1
            line += 1

    def check_gameover(self):
        for point in self.field.field[0]:
            if point:
                self.score_inf.check_record()
                self.score_inf.stop_count()
                return True
        return False
