import pygame
import constants


class InputBox:

    def __init__(self, text, font, screen, x, y, width, default: str, activate, min=6, max=50):
        self.font = font
        self.text = font.render(text, False, constants.COLORS['WHITE'])
        self.rect = self.text.get_rect(topleft=(x, y))
        self.input_rect = pygame.Rect(self.rect.right, self.rect.top, width, font.get_height())
        self.input = default
        self.screen = screen
        self.activate = activate
        self.min = min
        self.max = max

    def draw(self):
        self.screen.blit(self.text, self.rect)
        pygame.draw.line(self.screen, constants.COLORS['WHITE'], (self.rect.right, self.rect.bottom),
                         (self.rect.right + self.input_rect.width, self.rect.bottom), 5)
        self.screen.blit(self.font.render(self.input, False, constants.COLORS['WHITE']), self.input_rect)

    def click(self, event):
        if self.input_rect.collidepoint(event.pos):
            self.input = ''
            self.activate(self)

    def write(self, num: str):
        self.input += num

    def stop_input(self):
        if self.input == '':
            self.input = str(self.min)
        elif int(self.input) < self.min:
            self.input = str(self.min)
        elif int(self.input) > self.max:
            self.input = str(self.max)
