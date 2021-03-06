from InputFields.Button import Button
from InputFields.InputBox import InputBox
from Field import Field
from Pent import Pent
from Menu import Menu
from Settings import Settings
import constants
import pygame


class PentView:  # view

    def __init__(self):
        self.settings = Settings()
        self.time = 0
        self.clock = pygame.time.Clock()
        self.field = Field(self.settings.settings['field_width'], self.settings.settings['field_height'],
                           self.settings.settings['stop_color'])
        self.pent = Pent(self.field)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption('pent')
        pygame.display.set_icon(pygame.image.load(constants.ICON))
        self.gameover = False
        self.game_on = False
        self.menu_on = False
        buttons = {
            'restart': Button(self.restart, 'restart', pygame.font.Font(constants.FONT, 50), self.screen,
                              self.settings.window_width / 2, self.settings.window_height - 90),
            'reset_record': Button(self.reset_record, 'reset', pygame.font.Font(constants.FONT, 50),
                                   self.screen, 35 + 72, 170),
            'button_save_settings': Button(self.save_settings, 'save', pygame.font.Font(constants.FONT, 50),
                                           self.screen, 420, 67)
        }
        input_boxes = {
            'height': InputBox('height: ', pygame.font.Font(constants.FONT, 50), self.screen, 35, 35, 70,
                               str(self.settings.settings['field_height']), self.track_input_box, min=15, max=35),
            'width': InputBox('width: ', pygame.font.Font(constants.FONT, 50), self.screen, 35, 95, 70,
                              str(self.settings.settings['field_width']), self.track_input_box, min=10, max=20)
        }
        self.menu = Menu(buttons=buttons, input_boxes=input_boxes)
        self.active_input_box = None

    def restart(self):
        self.time = 0
        self.field = Field(self.settings.settings['field_width'], self.settings.settings['field_height'],
                           self.settings.settings['stop_color'])
        self.pent = Pent(self.field)
        self.menu_on = False

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover = True
                self.pent.score_inf.check_record()
                return
            if not self.menu_on:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # menu
                        self.menu_on = True
                        self.game_on = False
                        return
            if not self.gameover and not self.menu_on:
                if self.game_on:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.pent.set_direction(-1)
                        elif event.key == pygame.K_d:
                            self.pent.set_direction(1)
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
                        if event.key == pygame.K_a or event.key == pygame.K_d:
                            self.pent.set_direction(0)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_on = True
            elif self.menu_on:
                if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.menu.buttons.values():
                        button.click(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    for input_box in self.menu.input_boxes.values():
                        input_box.click(event)
                if event.type == pygame.KEYDOWN:
                    if self.active_input_box:
                        if event.key == pygame.K_0:
                            self.active_input_box.write('0')
                        if event.key == pygame.K_1:
                            self.active_input_box.write('1')
                        if event.key == pygame.K_2:
                            self.active_input_box.write('2')
                        if event.key == pygame.K_3:
                            self.active_input_box.write('3')
                        if event.key == pygame.K_4:
                            self.active_input_box.write('4')
                        if event.key == pygame.K_5:
                            self.active_input_box.write('5')
                        if event.key == pygame.K_6:
                            self.active_input_box.write('6')
                        if event.key == pygame.K_7:
                            self.active_input_box.write('7')
                        if event.key == pygame.K_8:
                            self.active_input_box.write('8')
                        if event.key == pygame.K_9:
                            self.active_input_box.write('9')
                        if event.key == pygame.K_BACKSPACE:
                            self.active_input_box.input = self.active_input_box.input[:-1]
                        if event.key == pygame.K_RETURN:
                            self.active_input_box.stop_input()
                            self.active_input_box = None
                    if event.key == pygame.K_ESCAPE:
                        self.menu_on = False
                        self.game_on = True

    def track_input_box(self, input_box):
        self.active_input_box = input_box

    def save_settings(self):
        new_settings = self.settings.default_settings
        self.menu.update()
        new_settings['field_width'] = int(self.menu.input_boxes['width'].input)
        new_settings['field_height'] = int(self.menu.input_boxes['height'].input)
        tmp = self.settings.window_width
        self.settings.update_settings(new_settings)
        self.menu.buttons['restart'].rect = self.menu.buttons['restart'].rect.move((self.settings.window_width - tmp) /
                                                                                   2, self.settings.window_height - 90 -
                                                                                   self.menu.buttons['restart'].rect.y)
        self.screen = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        self.restart()

    def reset_record(self):
        self.pent.score_inf.reset()

    def draw_menu(self):
        font = pygame.font.Font(constants.FONT, 50)
        text = font.render(self.menu.sentence, False, constants.COLORS['WHITE'])
        text_rect = text.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 2))
        self.screen.blit(text, text_rect)
        for button in self.menu.buttons.values():
            button.draw()
        for input_box in self.menu.input_boxes.values():
            input_box.draw()

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
        for i in range(self.settings.settings['field_width']):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH + i * constants.POINT_SIZE - 1,
                              constants.FRAME_THICKNESS),
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH + i * constants.POINT_SIZE - 1,
                              constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                              self.settings.settings['field_height'] * constants.POINT_SIZE), 2)
        for i in range(self.settings.settings['field_height']):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH, constants.FRAME_THICKNESS +
                              i * constants.POINT_SIZE - 1),
                             (constants.FRAME_THICKNESS + constants.SCORE_TABLE_WIDTH +
                              self.settings.settings['field_width'] * constants.POINT_SIZE - 1,
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
                                     (rect.left + point * constants.POINT_SIZE, rect.top + line * constants.POINT_SIZE,
                                      constants.POINT_SIZE, constants.POINT_SIZE))

        for i in range(constants.POINTS_PER_FIGURE + 1):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (rect.left + i * constants.POINT_SIZE - 1, rect.top),
                             (rect.left + i * constants.POINT_SIZE - 1, rect.bottom), 2)
        for i in range(constants.POINTS_PER_FIGURE + 1):
            pygame.draw.line(self.screen, constants.COLORS['BLACK'],
                             (rect.left, rect.top + i * constants.POINT_SIZE - 1),
                             (rect.left + constants.POINTS_PER_FIGURE * constants.POINT_SIZE - 1,
                              rect.top + i * constants.POINT_SIZE - 1), 2)

    def process_move(self):
        self.pent.move_figure(self.time)
        if not self.pent.fall_figure(self.time):
            self.game_on = False
            self.pent.score_inf.check_record()
            self.restart()

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
