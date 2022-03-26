import pygame


class Text(object):

    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = pygame.font.Font(textFont, size)
        self.render = self.font.render(message, True, color)
        self.rect = self.render.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    def draw(self, surface):
        surface.blit(self.render, self.rect)
