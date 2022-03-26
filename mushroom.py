

import pygame
from pygame.sprite import Sprite


class Mushroom(Sprite):
    def __init__(self, screen, settings, is_one_up = False):
        super(Mushroom, self).__init__()
        self.screen = screen
        self.settings = settings
        self.facing_left = False
        self.is_moving = False
        self.start_spawn = False
        self.is_falling = True
        self.is_one_up = is_one_up
        self.kill_flag = False
        if self.is_one_up:
            self.name = "One Up"
        else:
            self.name = "Mushroom"

        if self.is_one_up:
            self.image = pygame.transform.scale(pygame.image.load(settings.oneup_img),
                                                (settings.mushroom_width, settings.mushroom_height))
        else:
            self.image = pygame.transform.scale(pygame.image.load(settings.mushroom_img),
                                                (settings.mushroom_width, settings.mushroom_height))
        # self.image.fill((255, 255, 255, 150))
        self.rect = self.image.get_rect()
        self.initial_pos = (self.rect.x, self.rect.y)
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)
        self.wait_count = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

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
        pass

    def mark_for_death(self):
        self.kill_flag = True

    def update(self):
        # gravity
        # self.rect.centery += self.settings.gravity
        if self.start_spawn:
            print('mushroom target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
            if self.rect.y > self.target_pos[1]:
                self.rect.y = self.rect.y - self.settings.item_box_spawn_speed
            else:
                self.rect.y = self.target_pos[1]
                print('mushroom target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
                print('mushroom height: ' + str(self.rect.h))
                self.start_spawn = False
                self.wait_count = 0
                self.is_moving = True
        elif self.is_moving:
            self.wait_count += 1

        # item spawned wait X frames
        if self.is_moving and self.wait_count > 5:
            if self.facing_left and self.is_moving:
                self.rect.x -= self.settings.mushroom_speed
            elif self.is_moving:
                self.rect.x += self.settings.mushroom_speed

            if self.is_falling and self.is_moving:
                self.rect.bottom += self.settings.gravity

        #check to kill
        if self.kill_flag:
            self.kill()

