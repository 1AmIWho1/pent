from Field import Field
from Pent import Pent
import constants
import pygame


class PentView:  # view

    def __init__(self):
        self.time = 0
        self.clock = pygame.time.Clock()
        self.field = Field()
        self.pent = Pent(self.field)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((constants.FIELD_WIDTH * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS, constants.SCORE_TABLE_HEIGHT + constants.FIELD_HEIGHT * constants.POINT_SIZE + 2 * constants.FRAME_THICKNESS))
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
                                     (constants.FRAME_THICKNESS + constants.POINT_SIZE * point, constants.FRAME_THICKNESS + constants.POINT_SIZE * line, constants.POINT_SIZE, constants.POINT_SIZE))
                else:
                    pygame.draw.rect(self.screen, constants.COLORS['WHITE'],
                                     (constants.FRAME_THICKNESS + constants.POINT_SIZE * point, constants.FRAME_THICKNESS + constants.POINT_SIZE * line, constants.POINT_SIZE, constants.POINT_SIZE))

    def draw_figure(self):
        for line in range(len(self.pent.figure.shape)):
            for point in range(len(self.pent.figure.shape[line])):
                if self.pent.figure.shape[line][point]:
                    pygame.draw.rect(self.screen, self.pent.figure.color,
                                     (self.pent.figure_x + constants.POINT_SIZE * point, self.pent.figure_y + constants.POINT_SIZE * line, constants.POINT_SIZE, constants.POINT_SIZE))

    def draw_score(self):
        font = pygame.font.SysFont(constants.FONT, 34)
        text_score = font.render('score:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_score, (self.pent.score_inf.x, self.pent.score_inf.y))
        value_score = font.render(str(self.pent.score_inf.score), False, constants.COLORS['WHITE'])
        self.screen.blit(value_score, (self.pent.score_inf.x + 140, self.pent.score_inf.y))
        text_record = font.render('record:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_record, (self.pent.score_inf.x, self.pent.score_inf.y + 36))
        value_record = font.render(str(self.pent.score_inf.record), False, constants.COLORS['WHITE'])
        self.screen.blit(value_record, (self.pent.score_inf.x + 140, self.pent.score_inf.y + 36))

    def process_move(self):
        self.pent.fall_figure(self.time)

    def process_draw(self):
        self.screen.fill(constants.COLORS['BLACK'])
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
