from Field import Field
from Pent import Pent
from Menu import Menu
import constants
import pygame

from Button import Button


class PentView:  # view

    def __init__(self):
        self.time = 0
        self.clock = pygame.time.Clock()
        self.field = Field()
        self.menu = Menu()
        self.pent = Pent(self.field)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        pygame.display.set_caption('pent')
        self.gameover = False
        self.game_on = False
        self.menu_on = False
        self.button_restart = Button(self.restart, 'restart', pygame.font.Font(constants.FONT, 50), self.screen,
                                     constants.WINDOW_WIDTH / 2, 400)

    def restart(self):
        self.time = 0
        self.field = Field()
        self.pent = Pent(self.field)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover = True
                self.pent.score_inf.check_record()
            elif not self.gameover and not self.menu_on:
                if self.game_on:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # menu
                            self.menu_on = True
                            self.game_on = False
                        elif event.key == pygame.K_a:
                            self.pent.move_figure(-1)
                        elif event.key == pygame.K_d:
                            self.pent.move_figure(1)
                        elif event.key == pygame.K_q:
                            self.pent.rotate_figure(False)
                        elif event.key == pygame.K_e:
                            self.pent.rotate_figure(True)
                        elif event.key == pygame.K_s:
                            self.pent.accelerate_figure(True)
                        elif event.key == pygame.K_SPACE:
                            self.pent.drop_figure()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_s:
                            self.pent.accelerate_figure(False)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_on = True
            elif self.menu_on:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_restart.click(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_on = False

    def draw_menu(self):
        font = pygame.font.Font(constants.FONT, 50)
        text = font.render(self.menu.sentence, False, constants.COLORS['WHITE'])
        text_rect = text.get_rect(center=(constants.WINDOW_WIDTH / 2, constants.WINDOW_HEIGHT / 2))
        self.screen.blit(text, text_rect)

        self.button_restart.draw()

    def draw_field(self):
        for line in range(len(self.field.field)):
            for point in range(len(self.field.field[line])):
                if self.field.field[line][point]:
                    pygame.draw.rect(self.screen, self.field.field[line][point],
                                     (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                                      constants.POINT_SIZE * point, constants.FRAME_THICKNESS +
                                      constants.POINT_SIZE * line, constants.POINT_SIZE, constants.POINT_SIZE))
                else:
                    pygame.draw.rect(self.screen, constants.COLORS['WHITE'],
                                     (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                                      constants.POINT_SIZE * point, constants.FRAME_THICKNESS +
                                      constants.POINT_SIZE * line, constants.POINT_SIZE, constants.POINT_SIZE))

    def draw_figure(self):
        for line in range(len(self.pent.figure.shape)):
            for point in range(len(self.pent.figure.shape[line])):
                if self.pent.figure.shape[line][point]:
                    pygame.draw.rect(self.screen, self.pent.figure.color,
                                     (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                                      (self.pent.figure_x + point) * constants.POINT_SIZE,
                                      constants.FRAME_THICKNESS + (self.pent.figure_y + line) * constants.POINT_SIZE,
                                      constants.POINT_SIZE, constants.POINT_SIZE))

    def draw_grid(self):
        for i in range(constants.FIELD_WIDTH):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH + i * constants.POINT_SIZE - 1,
                              constants.FRAME_THICKNESS),
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH + i * constants.POINT_SIZE - 1,
                              constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                              constants.FIELD_HEIGHT * constants.POINT_SIZE), 2)
        for i in range(constants.FIELD_HEIGHT):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH, constants.FRAME_THICKNESS +
                              i * constants.POINT_SIZE - 1),
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                              constants.FIELD_WIDTH * constants.POINT_SIZE - 1,
                              constants.FRAME_THICKNESS + i * constants.POINT_SIZE - 1), 2)

    def draw_score(self):
        font = pygame.font.Font(constants.FONT, constants.FONT_SIZE)
        text_next = font.render('next:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_next, (constants.FRAME_THICKNESS + 10, constants.FRAME_THICKNESS + 25))
        text_score = font.render('score:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_score, (constants.FRAME_THICKNESS + 10, constants.FRAME_THICKNESS + 250))
        value_score = font.render(str(self.pent.score_inf.score), False, constants.COLORS['WHITE'])
        self.screen.blit(value_score, (constants.FRAME_THICKNESS + 10 + 140, constants.FRAME_THICKNESS + 250))
        text_record = font.render('record:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_record, (constants.FRAME_THICKNESS + 10,
                                       constants.FRAME_THICKNESS + 250 + constants.FONT_SIZE + 2))
        value_record = font.render(str(self.pent.score_inf.record), False, constants.COLORS['WHITE'])
        self.screen.blit(value_record, (constants.FRAME_THICKNESS + 10 + 140,
                                        constants.FRAME_THICKNESS + 250 + constants.FONT_SIZE + 2))
        text_solved = font.render('solved:', False, constants.COLORS['WHITE'])
        self.screen.blit(text_solved, (constants.FRAME_THICKNESS + 10,
                                       constants.FRAME_THICKNESS + 250 + 2 * (constants.FONT_SIZE + 2)))
        value_solved = font.render(str(self.pent.score_inf.solved), False, constants.COLORS['WHITE'])
        self.screen.blit(value_solved, (constants.FRAME_THICKNESS + 10 + 140,
                                        constants.FRAME_THICKNESS + 250 + 2 * (constants.FONT_SIZE + 2)))

    def draw_next(self):
        rect = pygame.Rect((0, 0, constants.POINT_SIZE * constants.POINTS_PER_FIGURE,
                            constants.POINT_SIZE * constants.POINTS_PER_FIGURE))
        rect.center = ((constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH) / 2, 150)
        pygame.draw.rect(self.screen, constants.COLORS['WHITE'], rect)

        for line in range(len(self.pent.next_figure.shape)):
            for point in range(len(self.pent.next_figure.shape[line])):
                if self.pent.next_figure.shape[line][point]:
                    pygame.draw.rect(self.screen, self.pent.next_figure.color,
                                     (rect.left + (point + len(self.pent.next_figure.shape) // 2) *
                                      constants.POINT_SIZE,
                                      rect.top + (line + len(self.pent.next_figure.shape[0]) // 2) *
                                      constants.POINT_SIZE, constants.POINT_SIZE, constants.POINT_SIZE))

        for i in range(constants.POINTS_PER_FIGURE):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (rect.left + i * constants.POINT_SIZE - 1, rect.top),
                             (rect.left + i * constants.POINT_SIZE - 1, rect.bottom), 2)
        for i in range(constants.POINTS_PER_FIGURE):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (rect.left, rect.top + i * constants.POINT_SIZE - 1),
                             (rect.left + constants.POINTS_PER_FIGURE * constants.POINT_SIZE - 1,
                              rect.top + i * constants.POINT_SIZE - 1), 2)

    def process_move(self):
        self.pent.fall_figure(self.time)

    def process_draw(self):
        self.screen.fill(constants.COLORS['BLACK'])
        if self.menu_on:
            self.draw_menu()
        else:
            self.draw_field()
            self.draw_figure()
            self.draw_next()
            if constants.GRID:
                self.draw_grid()
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
