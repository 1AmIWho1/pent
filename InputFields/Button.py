import pygame
import constants


class Button:

    def __init__(self, func, text, font, screen, x, y):
        self.text = font.render(text, False, constants.COLORS['WHITE'])
        self.rect = self.text.get_rect(midtop=(x, y))
        self.cur_color = constants.COLORS['BLACK']
        self.screen = screen
        self.func = func

    def draw(self):
        pygame.draw.rect(self.screen, constants.COLORS['WHITE'], self.rect.inflate(15, 15))
        pygame.draw.rect(self.screen, self.cur_color, self.rect.inflate(5, 5))
        self.screen.blit(self.text, self.rect)

    def click(self, event):
        if self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.cur_color = constants.COLORS['PINK']
            if event.type == pygame.MOUSEBUTTONUP:
                self.func()
                self.cur_color = constants.COLORS['BLACK']
