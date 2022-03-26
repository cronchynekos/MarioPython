

import pygame
from pygame.sprite import Sprite


class Goomba(Sprite):

    def __init__(self, screen, settings):
        super(Goomba, self).__init__()
        self.settings = settings
        self.screen = screen
        self.name = "Goomba"

        self.facing_left = True
        self.hit_wall = False
        self.fall = False
        self.is_dead = False

        self.index = 0
        self.last_tick = pygame.time.get_ticks()
        self.death_timer = pygame.time.get_ticks()

        self.image = pygame.transform.scale(pygame.image.load("Images/goomba_2.png"),
                                            (self.settings.goomba_width, self.settings.goomba_height))

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.images = []
        self.images.extend([pygame.transform.scale(pygame.image.load("Images/goomba_2.png"),
                                                   (self.settings.goomba_width, self.settings.goomba_height)),
                            pygame.transform.scale(pygame.image.load("Images/goomba_1.png"),
                                                   (self.settings.goomba_width, self.settings.goomba_height))])
        # self.dead_image = pygame.transform.scale(pygame.image.load("Images/goomba_death.png"))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    # def set_pos(self, top, left):
    #     self.rect.top = top * self.settings.goomba_height
    #     self.rect.left = left * self.settings.goomba_width
    # Copied and modified from block.py, checks for goomba collision

    def check_collision(self):
        self.collision_pts = {
            "topSide": [self.rect.top, self.rect.midtop, self.rect.topright],
            "rightSide": [self.rect.topright, self.rect.midright, self.rect.bottomright],
            "leftSide": [self.rect.topleft, self.rect.midleft, self.rect.bottomleft],
            "bottomSide": [self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright]
        }
        return self.collision_pts

    def dead(self):
        self.settings.score_holder += self.settings.point_values['goomba']
        self.image = pygame.transform.scale(pygame.image.load("Images/goomba_death.png"),
                                            (self.settings.goomba_width, self.settings.goomba_height))
        self.death_timer = pygame.time.get_ticks()
        self.is_dead = True

    def update(self):
        if self.is_dead:
            self.kill()
            return
        if self.rect.colliderect(self.screen.get_rect()):
            self.iterate_index(len(self.images))
            self.image = self.images[self.index]

            # gravity
            self.rect.y += self.settings.gravity

            if self.facing_left:
                self.rect.x -= 1
            else:
                self.rect.x += 1

    def iterate_index(self, max_):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 200:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()

        if self.index == max_:
            self.index = 0
