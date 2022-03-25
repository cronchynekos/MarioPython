import pygame

class ImageRect:
    def __init__(self, screen, imagename, height, width):
        self.screen = screen
        name = imagename

        img = pygame.image.load(name).convert_alpha()
        self.rect = img.get_rect()
        self.rect.left -= self.rect.width
        self.rect.top -= self.rect.height
        self.image = img

    def blit(self) : self.screen.blit (self.image, self.rect)