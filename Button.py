import pygame
import constants


class Button:

    def __init__(self, func, text, font, screen, x, y):
        self.text = font.render(text, False, constants.COLORS['WHITE'])
        self.screen = screen
        self.rect = self.text.get_rect(midtop=(x, y))
        self.func = func

    def draw(self):
        pygame.draw.rect(self.screen, constants.COLORS['WHITE'], self.rect.inflate(15, 15))
        pygame.draw.rect(self.screen, constants.COLORS['BLACK'], self.rect.inflate(5, 5))
        self.screen.blit(self.text, self.rect)

    def click(self, event):
        if self.rect.collidepoint(event.pos):
            self.func()
