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
        self.figure_x = constants.FRAME_THICKNESS + (
                    (constants.FIELD_WIDTH - len(self.figure.shape[0])) // 2) * constants.POINT_SIZE
        self.figure_y = constants.FRAME_THICKNESS

    def add_new_figure(self):  # добавляет новую фигуру сверху посередине
        self.accelerate_figure(False)
        self.figure = Figure()
        self.figure_x = constants.FRAME_THICKNESS + ((constants.FIELD_WIDTH - len(self.figure.shape[0])) // 2) * constants.POINT_SIZE  # что это блять?
        self.figure_y = constants.FRAME_THICKNESS

    def stop_figure(self):  # останавливает фигуру и записывает ее в поле
        x = (self.figure_x - constants.FRAME_THICKNESS) // constants.POINT_SIZE
        y = (self.figure_y - constants.FRAME_THICKNESS) // constants.POINT_SIZE
        for line in range(y, y + len(self.figure.shape)):
            for point in range(len(self.figure.shape[0])):
                if self.figure.shape[line - y][point]:
                    try:
                        self.field.field[line][x + point] = True
                    except IndexError:
                        pass
        self.score_inf.update(constants.POINTS_PER_STOP)

    def move_figure(self, direction):  # движение фигуры влево/вправо
        if direction == -1 and not self.check_collision_left():
            self.figure_x += direction * constants.POINT_SIZE
        elif direction == 1 and not self.check_collision_right():
            self.figure_x += direction * constants.POINT_SIZE

    def rotate_figure(self, direction: bool):  # вращение фигуры по/против часовой стрелке
        self.figure.rotate(direction)
        if self.check_collision_left() or self.check_collision_right() or self.check_collision_down():
            self.figure.rotate(not direction)

    def accelerate_figure(self, acc):  # ускорение фигуры
        if acc:
            self.time_per_move = constants.ACCELERATE_TIME_PER_MOVE
        else:
            self.time_per_move = constants.TIME_PER_MOVE

    def fall_figure(self, time):  # нормальное падение фигуры
        collision = self.check_collision_down()
        if not collision and time - self.last_time >= self.time_per_move:
            self.figure_y += constants.POINT_SIZE
            self.last_time = time
        elif collision:
            self.stop_figure()
            self.add_new_figure()

    def check_collision_left(self):
        if constants.FRAME_THICKNESS >= self.figure_x:
            return True
        try:
            x = (self.figure_x - constants.FRAME_THICKNESS) // constants.POINT_SIZE
            y = (self.figure_y - constants.FRAME_THICKNESS) // constants.POINT_SIZE
            line = y
            while line < y + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):
                    if self.figure.shape[line - y][point] and self.field.field[line][x + point - 1]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_right(self):
        if self.figure_x + len(self.figure.shape[0]) * constants.POINT_SIZE >= constants.FRAME_THICKNESS + constants.FIELD_WIDTH * constants.POINT_SIZE:
            return True
        try:
            x = (self.figure_x - constants.FRAME_THICKNESS) // constants.POINT_SIZE
            y = (self.figure_y - constants.FRAME_THICKNESS) // constants.POINT_SIZE
            line = y
            while line < y + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):
                    if self.figure.shape[line - y][point] and self.field.field[line][x + point + 1]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_collision_down(self):
        if self.figure_y + len(self.figure.shape) * constants.POINT_SIZE >= constants.FRAME_THICKNESS + len(self.field.field) * constants.POINT_SIZE:
            return True
        try:
            x = (self.figure_x - constants.FRAME_THICKNESS) // constants.POINT_SIZE
            y = (self.figure_y - constants.FRAME_THICKNESS) // constants.POINT_SIZE + 1
            line = y
            while line < y + len(self.figure.shape):
                for point in range(len(self.figure.shape[0])):
                    if self.figure.shape[line - y][point] and self.field.field[line][x + point]:
                        return True
                line += 1
        except IndexError:
            return True
        return False

    def check_and_stop(self):
        line = 0
        while line < len(self.field.field):
            if self.field.field[line] == [True for i in range(constants.FIELD_WIDTH)]:
                self.score_inf.update(constants.POINTS_PER_LINE)
                for item in range(line, 0, -1):
                    self.field.field[item] = self.field.field[item - 1]
                self.field.field[0] = [False for i in range(constants.FIELD_WIDTH)]
                line -= 1
            line += 1

    def check_gameover(self):
        for point in self.field.field[0]:
            if point:
                self.score_inf.check_record()
                self.score_inf.stop_count()
                return True
        return False
