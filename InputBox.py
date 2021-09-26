import pygame
import constants


class InputBox:

    def __init__(self, text, font, screen, x, y, width):
        self.text = font.render(text, False, constants.COLORS['WHITE'])
        self.rect = self.text.get_rect(topleft=(x, y))
        self.input_rect = pygame.Rect(self.rect.right, self.rect.top, width, font.get_height())
        self.screen = screen

    def draw(self):
        self.screen.blit(self.text, self.rect)
        pygame.draw.line(self.screen, constants.COLORS['WHITE'], (self.rect.right, self.rect.bottom),
                         (self.rect.right + self.input_rect.width, self.rect.bottom), 5)
