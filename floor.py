
import pygame
from pygame import image
# from pygame.sprite import Sprite
from block import Block


class Floor(Block):

    def __init__(self, screen, settings, is_underground=False):
        super(Floor, self).__init__(screen, settings, is_underground=is_underground)
        self.screen = screen
        self.settings = settings
        self.image = None

        if is_underground:
            self.image = pygame.transform.scale(
                image.load(settings.floor_ug_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )
        else:
            self.image = pygame.transform.scale(
                image.load(settings.floor_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
        )
        self.rect = self.image.get_rect()
        self.collision_pts = self.get_collision_points()


    def draw(self):
        self.screen.blit(self.image, self.rect)
