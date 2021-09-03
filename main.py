import pygame
import random
import json
import numpy as np

POINTS_PER_FIGURE = 5

FIELD_WIDTH = 15
FIELD_HEIGHT = 20

SCORE_TABLE_HEIGHT = 100

FRAME_THICKNESS = 10
POINT_SIZE = 25

TIME_PER_MOVE = 400
ACCELERATE_TIME_PER_MOVE = 100

POINTS_PER_STOP = 10
POINTS_PER_LINE = 100

FONT = 'progresspixel-bold'

COLORS = {
    'RED': pygame.Color(255, 0, 0),
    'WHITE': pygame.Color(255, 255, 255),
    'BLACK': pygame.Color(0, 0, 0),
    'BLUE': pygame.Color(0, 0, 153),
    'GREEN': pygame.Color(51, 102, 0),
    'STOP_COLOR': pygame.Color(0, 0, 51),
}


def get_random_color(expectations):
    colors_keys = list(COLORS.keys())
    if isinstance(expectations, list):
        for expectation in expectations:
            colors_keys.remove(expectation)
    else:
        colors_keys.remove(expectations)
    return COLORS[random.choice(colors_keys)]


class Figure:

    def __init__(self):
        self.shape = [[False for i in range(POINTS_PER_FIGURE)] for i in range(POINTS_PER_FIGURE)]
        self.color = get_random_color(['WHITE', 'STOP_COLOR', 'BLACK'])
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

    def rotate(self, direction):
        if direction == 1:
            self.shape = np.rot90(self.shape)
        else:
            for i in range(3):
                self.shape = np.rot90(self.shape)


class Field:  # model

    def __init__(self):
        self.field = [[False for i in range(FIELD_WIDTH)] for i in range(FIELD_HEIGHT)]
        self.color_stopped_figures = COLORS['STOP_COLOR']


class Score:

    def __init__(self):
        self.score = 0
        try:
            with open('record.json', 'r') as r:
                self.record = json.load(r)
        except FileNotFoundError:
            with open('record.json', 'w') as r:
                json.dump(0, r)
            self.record = 0
        self.x = 25
        self.y = FIELD_HEIGHT * POINT_SIZE + 2 * FRAME_THICKNESS - 5

    def update(self, points):
        self.score += points

    def stop_count(self):
        self.score = 0

    def check_record(self):
        if self.score > self.record:
            with open('record.json', 'w') as record_json:
                json.dump(self.score, record_json)
            return True
        return False


class Pent:  # controller

    def __init__(self, field: Field):
        self.last_time = 0
        self.field = field
        self.time_per_move = TIME_PER_MOVE
        self.add_new_figure()
        self.score_inf = Score()

    def add_new_figure(self):
        self.accelerate_figure(False)
        self.figure = Figure()
        self.figure_x = FRAME_THICKNESS + ((FIELD_WIDTH - len(self.figure.shape[0])) // 2 + 1) * POINT_SIZE
        self.figure_y = FRAME_THICKNESS

    def stop_figure(self):
        x = (self.figure_x - FRAME_THICKNESS) // POINT_SIZE
        y = (self.figure_y - FRAME_THICKNESS) // POINT_SIZE
        for line in range(y, y + len(self.figure.shape)):
            for point in range(len(self.figure.shape[0])):
                if self.figure.shape[line - y][point]:
                    try:
                        self.field.field[line][x + point] = True
                    except IndexError:
                        pass
        self.score_inf.update(POINTS_PER_STOP)

    def move_figure(self, direction):
        if direction == -1 and not self.check_collision_left():
            self.figure_x += direction * POINT_SIZE
        elif direction == 1 and not self.check_collision_right():
            self.figure_x += direction * POINT_SIZE

    def rotate_figure(self, direction):
        if not self.check_collision_left() and not self.check_collision_right() and not self.check_collision_down():
            self.figure.rotate(direction)

    def accelerate_figure(self, acc):
        if acc:
            self.time_per_move = ACCELERATE_TIME_PER_MOVE
        else:
            self.time_per_move = TIME_PER_MOVE

    def fall_figure(self, time):
        collision = self.check_collision_down()
        if not collision and time - self.last_time >= self.time_per_move:
            self.figure_y += POINT_SIZE
            self.last_time = time
        elif collision:
            self.stop_figure()
            self.add_new_figure()

    def check_collision_left(self):
        if FRAME_THICKNESS >= self.figure_x:
            return True
        try:
            x = (self.figure_x - FRAME_THICKNESS) // POINT_SIZE
            y = (self.figure_y - FRAME_THICKNESS) // POINT_SIZE
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
        if self.figure_x + len(self.figure.shape[0]) * POINT_SIZE >= FRAME_THICKNESS + FIELD_WIDTH * POINT_SIZE:
            return True
        try:
            x = (self.figure_x - FRAME_THICKNESS) // POINT_SIZE
            y = (self.figure_y - FRAME_THICKNESS) // POINT_SIZE
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
        if self.figure_y + len(self.figure.shape) * POINT_SIZE >= FRAME_THICKNESS + len(self.field.field) * POINT_SIZE:
            return True
        try:
            x = (self.figure_x - FRAME_THICKNESS) // POINT_SIZE
            y = (self.figure_y - FRAME_THICKNESS) // POINT_SIZE + 1
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
            if self.field.field[line] == [True for i in range(FIELD_WIDTH)]:
                self.score_inf.update(POINTS_PER_LINE)
                for item in range(line, 0, -1):
                    self.field.field[item] = self.field.field[item - 1]
                self.field.field[0] = [False for i in range(FIELD_WIDTH)]
                line -= 1
            line += 1

    def check_gameover(self):
        for point in self.field.field[0]:
            if point:
                self.score_inf.check_record()
                self.score_inf.stop_count()
                return True
        return False


class PentView:  # view

    def __init__(self):
        self.time = 0
        self.clock = pygame.time.Clock()
        self.field = Field()
        self.pent = Pent(self.field)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((FIELD_WIDTH * POINT_SIZE + 2 * FRAME_THICKNESS, SCORE_TABLE_HEIGHT + FIELD_HEIGHT * POINT_SIZE + 2 * FRAME_THICKNESS))
        self.gameover = False
        self.game_on = False

    def restart(self):
        self.time = 0
        self.field = Field()
        self.pent = Pent(self.field)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover = True
                self.pent.score_inf.check_record()
            elif not self.gameover:
                if self.game_on:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # may be a menu?
                            self.gameover = True
                            self.pent.score_inf.check_record()
                        elif event.key == pygame.K_a:
                            self.pent.move_figure(-1)
                        elif event.key == pygame.K_d:
                            self.pent.move_figure(1)
                        elif event.key == pygame.K_q:
                            self.pent.rotate_figure(-1)
                        elif event.key == pygame.K_e:
                            self.pent.rotate_figure(1)
                        elif event.key == pygame.K_s:
                            self.pent.accelerate_figure(True)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_s:
                            self.pent.accelerate_figure(False)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_on = True

    def draw_field(self):
        for line in range(len(self.field.field)):
            for point in range(len(self.field.field[line])):
                if self.field.field[line][point]:
                    pygame.draw.rect(self.screen, self.field.color_stopped_figures,
                                     (FRAME_THICKNESS + POINT_SIZE * point, FRAME_THICKNESS + POINT_SIZE * line, POINT_SIZE, POINT_SIZE))
                else:
                    pygame.draw.rect(self.screen, COLORS['WHITE'],
                                     (FRAME_THICKNESS + POINT_SIZE * point, FRAME_THICKNESS + POINT_SIZE * line, POINT_SIZE, POINT_SIZE))

    def draw_figure(self):
        for line in range(len(self.pent.figure.shape)):
            for point in range(len(self.pent.figure.shape[line])):
                if self.pent.figure.shape[line][point]:
                    pygame.draw.rect(self.screen, self.pent.figure.color,
                                     (self.pent.figure_x + POINT_SIZE * point, self.pent.figure_y + POINT_SIZE * line, POINT_SIZE, POINT_SIZE))

    def draw_score(self):
        font = pygame.font.SysFont(FONT, 34)
        text_score = font.render('score:', False, COLORS['WHITE'])
        self.screen.blit(text_score, (self.pent.score_inf.x, self.pent.score_inf.y))
        value_score = font.render(str(self.pent.score_inf.score), False, COLORS['WHITE'])
        self.screen.blit(value_score, (self.pent.score_inf.x + 140, self.pent.score_inf.y))
        text_record = font.render('record:', False, COLORS['WHITE'])
        self.screen.blit(text_record, (self.pent.score_inf.x, self.pent.score_inf.y + 36))
        value_record = font.render(str(self.pent.score_inf.record), False, COLORS['WHITE'])
        self.screen.blit(value_record, (self.pent.score_inf.x + 140, self.pent.score_inf.y + 36))

    def process_move(self):
        self.pent.fall_figure(self.time)

    def process_draw(self):
        self.screen.fill(COLORS['BLACK'])
        self.draw_field()
        self.draw_figure()
        self.draw_score()
        pygame.display.flip()

    def process_check(self):
        self.pent.check_and_stop()
        if self.pent.check_gameover():
            self.game_on = False
            self.restart()

    def process_logic(self):
        if self.game_on:
            self.time += self.clock.tick()
            self.process_move()
            self.process_check()

    def loop(self):
        while not self.gameover:
            self.process_draw()
            self.process_events()
            self.process_logic()
            pygame.time.wait(10)


def main():
    view = PentView()
    view.loop()


if __name__ == '__main__':
    main()
