

import pygame
from pygame.sprite import Sprite
from shell import Shell


class Koopa(Sprite):

    def __init__(self, screen, settings):
        super(Koopa, self).__init__()
        self.name = "Koopa"
        self.screen = screen
        self.index = 0
        self.settings = settings
        self.hit_wall = False
        self.fall = False
        self.is_dead = False
        self.facing_left = True
        self.death_timer = -900
        self.last_tick = pygame.time.get_ticks()

        self.image = pygame.transform.scale(pygame.image.load("Images/koopa_2.png"),
                                            (self.settings.koopa_width, self.settings.koopa_height))

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.images = []
        self.images.extend([pygame.transform.scale(pygame.image.load("Images/koopa_2.png"),
                                                   (self.settings.koopa_width, self.settings.koopa_height)),
                           pygame.transform.scale(pygame.image.load("Images/koopa_1.png"),
                                                  (self.settings.koopa_width, self.settings.koopa_height))])

    def update(self):
        if self.is_dead:
            self.kill()
            return

        if self.rect.colliderect(self.screen.get_rect()):
            self.iterate_index(len(self.images))
            self.image = self.images[self.index]
            self.rect.centery += self.settings.gravity

            if self.facing_left:
                self.rect.centerx -= 1
            else:
                self.rect.centerx += 1

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def dead(self, map_group=None, enemy_group=None, fireball_group=None):
        self.settings.score_manager += self.settings.point_values['koopa']
        self.is_dead = True

        if map_group != None and enemy_group != None and fireball_group != None:
            s = Shell(self.screen, self.settings, self.rect.centerx, self.rect.centery)
            s.add(map_group, enemy_group, fireball_group)

    def iterate_index(self, max_):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 200:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index == max_:
            self.index = 0
