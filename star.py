
import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    def __init__(self, screen, settings):
        super(Star, self).__init__()
        self.name = "Star"
        self.screen = screen
        self.settings = settings

        self.facing_left = False
        self.is_falling = False
        self.kill_flag = False
        self.is_moving = False
        self.start_spawn = False

        self.index = 0
        self.last_tick = pygame.time.get_ticks()

        self.image = pygame.transform.scale(pygame.image.load("Images/white.png"),
                                            (self.settings.star_width, self.settings.star_height))

        self.rect = self.image.get_rect()
        self.initial_pos = (self.rect.x, self.rect.y)
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)
        self.wait_count = 0
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
        self.screen.blit(pygame.transform.flip(self.image, self.facing_left, False), self.rect)

    def spawn(self):
        self.start_spawn = True

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
        self.kill_flag = True

    def update(self):
        self.iterate_index(len(self.images))
        self.image = self.images[self.index]

        if self.start_spawn:
            # print('star target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
            if self.rect.y > self.target_pos[1]:
                self.rect.y = self.rect.y - self.settings.item_box_spawn_speed
            else:
                self.rect.y = self.target_pos[1]
                # print('star target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
                # print('star height: ' + str(self.rect.h))
                self.start_spawn = False
                self.set_initial_max_jump_height()
                self.wait_count = 0
                self.is_moving = True
        elif self.is_moving and self.wait_count <= 5:
            self.wait_count += 1

        if self.is_moving and self.wait_count > 5:
            if self.facing_left:
                self.rect.centerx -= self.settings.star_speed
            else:
                self.rect.centerx += self.settings.star_speed

            if self.is_falling:
                self.rect.centery += self.settings.star_jump
            elif not self.is_falling and self.rect.centery < self.max_jump_height:
                # hit top limit
                self.is_falling = True
            elif not self.is_falling:
                self.rect.centery -= self.settings.star_jump


    def iterate_index(self, max):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()

            # temporarily placed movement in iterate, should belong in its own function
            # if self.is_falling:
            #     self.rect.centery += self.settings.star_jump
            # else:
            #     self.rect.centery -= self.settings.star_jump
        if self.index == max:
            self.index = 0
            # self.is_falling = not self.is_falling
