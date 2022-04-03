

import pygame
from pygame.sprite import Sprite

class Flag(Sprite):
    def __init__(self, screen, settings, xpos, ypos):
        super(Flag, self).__init__()
        self.screen = screen
        self.settings = settings

        self.raise_flag = False

        self.image = pygame.transform.scale(pygame.image.load("Images/flagpole.png"),
                                                    (self.settings.flag_width, self.settings.flag_height))
        self.rect = self.image.get_rect()
        self.rect.left = xpos
        self.rect.bottom = ypos

        self.flag_image = pygame.transform.scale(pygame.image.load("Images/flag.png"),
                                                 (self.settings.block_width - 2, self.settings.block_height))
        self.flag_rect = self.flag_image.get_rect()
        self.flag_rect.left = xpos - self.settings.block_width / 2
        self.flag_rect.bottom = ypos - self.settings.block_height

    def update(self):
        self.flag_rect.left = self.rect.left - self.settings.block_width / 2
        if self.raise_flag:
            self.flag_rect.top -= self.settings.flag_speed
            if self.flag_rect.top < self.rect.top + 24:
                self.flag_rect.top = self.rect.top + 24

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def draw_flag(self):
        if self.raise_flag:
            self.screen.blit(self.flag_image, self.flag_rect)