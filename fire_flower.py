
import pygame
from pygame.sprite import Sprite


class Fire_Flower(Sprite):
    def __init__(self, screen, settings):
        super(Fire_Flower, self).__init__()
        self.screen = screen
        self.settings = settings
        self.facing_left = False
        self.is_moving = False
        self.start_spawn = False
        self.is_falling = False
        self.kill_flag = False
        self.name = "Fire Flower"

        self.index = 0
        self.last_tick = pygame.time.get_ticks()

        self.image = pygame.transform.scale(pygame.image.load("Images/white.png"),
                                            (self.settings.fire_flower_width, self.settings.fire_flower_height))

        self.rect = self.image.get_rect()
        self.initial_pos = (self.rect.x, self.rect.y)
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)
        self.wait_count = 0

        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("Images/fire_flower_1.png"),
                                                  (self.settings.fire_flower_width, self.settings.fire_flower_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/fire_flower_2.png"),
                                                  (self.settings.fire_flower_width, self.settings.fire_flower_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/fire_flower_3.png"),
                                                  (self.settings.fire_flower_width, self.settings.fire_flower_height)))
        self.images.append(pygame.transform.scale(pygame.image.load("Images/fire_flower_4.png"),
                                                  (self.settings.fire_flower_width, self.settings.fire_flower_height)))

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

    def mark_for_death(self):
        self.kill_flag = True

    def update(self):
        self.iterate_index(len(self.images))
        self.image = self.images[self.index]

        # Position Code:
        if self.start_spawn:
            if self.start_spawn:
                # print('fflower target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
                if self.rect.y > self.target_pos[1]:
                    self.rect.y = self.rect.y - self.settings.item_box_spawn_speed
                else:
                    self.rect.y = self.target_pos[1]
                    # print('fflower target y: ' + str(self.target_pos[1]) + ' actual y: ' + str(self.rect.y))
                    # print('fflower height: ' + str(self.rect.h))
                    self.start_spawn = False

    def iterate_index(self, max):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index == max:
            self.index = 0
