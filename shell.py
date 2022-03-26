

import pygame
from pygame.sprite import Sprite


class Shell(Sprite):

    def __init__(self, screen, settings, xpos, ypos):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.fall = False
        self.active = False
        self.hit_wall = False
        self.is_dead = False
        self.is_moving = True
        self.facing_left = False
        self.name = "Shell"
        self.death_timer = -1000

        self.image = pygame.transform.scale(pygame.image.load("Images/koopa_shell.png"),
                                            (self.settings.koopa_width, self.settings.koopa_width))
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.centery = ypos

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.is_dead:
            return
        if self.active:
            if self.facing_left:
                self.rect.centerx -= self.settings.shell_speed
            else:
                self.rect.centerx += self.settings.shell_speed
