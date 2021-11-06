from Figure import Figure
from Field import Field
from Score import Score
import constants


class Pent:  # controller

    def __init__(self, field: Field):
        self.last_time_fall = 0
        self.last_time_move = 0
        self.direction = 0
        self.field = field
        self.time_per_fall = constants.TIME_PER_FALL
        self.time_per_move = constants.TIME_PER_MOVE
        self.score_inf = Score()
        self.accelerate_figure(False)
        self.figure = Figure()
        self.next_figure = Figure()
        self.figure_x = (self.field.width - len(self.figure.shape[0])) // 2  # левая точка фигуры
        self.figure_y = -self.figure.get_empty_top()  # верхняя точка фигуры

    def add_new_figure(self):  # добавляет новую фигуру сверху посередине
        self.accelerate_figure(False)
        self.figure = self.next_figure
        self.next_figure = Figure()
        self.figure_x = (self.field.width - len(self.figure.shape[0])) // 2
        self.figure_y = 0

    def stop_figure(self):  # останавливает фигуру и записывает ее в поле
        self.field.add_figure(self.figure, self.figure_x, self.figure_y)
        self.score_inf.update(constants.POINTS_PER_STOP)

    def set_direction(self, direction):
        self.direction = direction
        if direction == 0:
            self.last_time_move = 0

    def move_figure(self, time):  # движение фигуры влево/вправо
        if time - self.last_time_move >= self.time_per_move:
            self.figure_x += self.direction
            if self.check_collision_right() or self.check_collision_left() or self.check_collision_down():
                self.figure_x -= self.direction
                return
            self.last_time_move = time

    def rotate_figure(self, direction: bool):  # вращение фигуры по/против часовой стрелке
        self.figure.rotate(direction)
        if self.check_collision_left() or self.check_collision_right() or self.check_collision_down():
            self.figure.rotate(not direction)

    def accelerate_figure(self, acc):  # ускорение фигуры
        if acc:
            self.time_per_fall = constants.ACCELERATE_TIME_PER_MOVE
        else:
            self.time_per_fall = constants.TIME_PER_FALL

    def drop_figure(self):  # мгновенное падение фигуры
        while not self.check_collision_down():
            self.figure_y += 1
        self.stop_figure()
        self.add_new_figure()

    def fall_figure(self, time):  # нормальное падение фигуры
        collision = self.check_collision_down()
        if not collision and time - self.last_time_fall >= self.time_per_fall:
            self.figure_y += 1
            self.last_time_fall = time
        elif collision:
            self.stop_figure()
            self.add_new_figure()
        '''
        for i in range(len(self.field.field)):
            for j in range(len(self.field.field[0])):
                if self.figure_y <= i < self.figure_y + constants.POINTS_PER_FIGURE and self.figure_x <= j < self.figure_x + constants.POINTS_PER_FIGURE:
                    if self.figure.shape[i - self.figure_y][j - self.figure_x]:
                        print('X', end='')
                    else:
                        print('-', end='')
                else:
                    if self.field.field[i][j]:
                        print('O', end='')
                    else:
                        print('_', end='')
            print()
        print()
        '''

    def check_collision_left(self):  # проверяет, не наезжает ли одна движущаяся фигура на что-либо слева
        if 0 > self.figure_x + self.figure.get_empty_left():
            return True
        try:
            line = self.figure_y
            empty_left = self.figure.get_empty_left()
            max_width = self.figure.get_width()
            while line < self.figure_y + self.figure.get_height():
                for point in range(empty_left + 1, empty_left + max_width):
                    if self.figure.shape[line - self.figure_y][point] and self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_right(self):    # проверяет, не наезжает ли одна движущаяся фигура на что-либо справа
        if self.figure_x + self.figure.get_empty_right() > self.field.width:
            return True
        try:
            line = self.figure_y
            empty_left = self.figure.get_empty_left()
            max_width = self.figure.get_width()
            while line < self.figure_y + len(self.figure.shape):
                for point in range(empty_left, empty_left + max_width):
                    if self.figure.shape[line - self.figure_y][point] and self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_down(self):
        if self.figure_y - self.figure.get_empty_top() + self.figure.get_height() > self.field.height:
            return True
        try:
            empty_left = self.figure.get_empty_left()
            max_width = self.figure.get_width()
            line = self.figure_y + 1
            while line < self.figure_y + 1 + len(self.figure.shape):
                for point in range(empty_left, empty_left + max_width):
                    if self.figure.shape[line - self.figure_y - 1][point] and \
                            self.field.field[line][self.figure_x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_and_stop(self):
        line = 0
        while line < self.field.height:
            try:
                self.field.field[line].index(False)
            except ValueError:
                self.score_inf.update(constants.POINTS_PER_LINE)
                self.score_inf.solve()
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
