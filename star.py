import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    def __init__(self, screen, settings):
        super(Star, self).__init__()
        self.name = "Star"
        self.screen = screen
        self.settings = settings
        self.index = 0
        self.last_tick = pygame.time.get_ticks()
        self.moving = False
        self.spawn = False

        self.facingL = False
        self.falling = False
        self.flag = False


        self.image = pygame.transform.scale(pygame.image.load("Images/white.png"),
                                            (self.settings.star_width, self.settings.star_height))

        self.rect = self.image.get_rect()
        self.initial_pos = (self.rect.x, self.rect.y)
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)
        self.wCount = 0
        self.set_max_jump_height()

        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("Images/star_1.png"),
                                                  (self.settings.star_width, self.settings.star_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/star_2.png"),
                                                  (self.settings.star_width, self.settings.star_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/star_3.png"),
                                                  (self.settings.star_width, self.settings.star_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/star_4.png"),
                                                  (self.settings.star_width, self.settings.star_height)))

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.facingL, False), self.rect)

    def spawn(self):
        self.spawn = True

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, y, x ):
        self.rect.top = y
        self.rect.left = x
        self.initial_pos = self.get_position()
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)

    def set_max_jump_height(self):
        self.max_jump_height = self.rect.centery - self.settings.star_max_jump_height

    def set_initial_max_jump_height(self):
        self.max_jump_height = self.rect.centery - self.settings.star_max_jump_height/3

    def mark_for_death(self):
        self.flag = True

    def update(self):
        self.iterate_index(len(self.images))
        self.image = self.images[self.index]

        if self.spawn:
            if self.rect.y > self.target_pos[1]:
                self.rect.y = self.rect.y - self.settings.item_spawn_speed
            else:
                self.wCount = 0
                self.set_initial_max_jump_height()
                self.rect.y = self.target_pos[1]
                self.spawn = False
                self.moving = True
        elif self.moving and self.wCount <= 5:
            self.wCount += 1

        if self.moving and self.wCount > 5:
            if self.facingL:
                self.rect.centerx -= self.settings.star_speed
            else:
                self.rect.centerx += self.settings.star_speed

            if self.falling:
                self.rect.centery += self.settings.star_jump
            elif not self.falling and self.rect.centery < self.max_jump_height:
                self.falling = True
            elif not self.falling:
                self.rect.centery -= self.settings.star_jump

    def iterate_index(self, max):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()

        if self.index == max:
            self.index = 0
