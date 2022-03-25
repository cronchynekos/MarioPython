import pygame

class SpriteSheet:

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_get(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        transparent_color = image.get_at((0, 0))
        image.set_colorkey(transparent_color)
        return image