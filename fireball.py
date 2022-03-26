import pygame
from pygame.sprite import Sprite


class Fireball(Sprite):
    # Class to manage fireballs

    def __init__(self, screen, settings, xpos, ypos):
        # Create fireball where Mario currently is
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.facing_left = False
        self.is_falling = True
        self.is_moving = True
        self.bounces = 0
        self.explode = False
        self.index = 0
        self.explosion_index = 0
        self.last_tick = pygame.time.get_ticks()
        self.name = "Fireball"

        self.image = pygame.transform.scale(pygame.image.load("Images/fireball_1.png"),
                                            (self.settings.fireball_width, self.settings.fireball_height))
        self.rect = self.image.get_rect()
        self.set_position(ypos, xpos)
        self.initial_pos = (self.rect.left, self.rect.top)
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)
        self.wait_count = 0
        self.max_jump_height = 0
        self.set_max_jump_height()

        # Images for fireball
        self.images = []
        self.images.extend([pygame.transform.scale(pygame.image.load("Images/fireball_1.png"),
                                                   (self.settings.fireball_width, self.settings.fireball_height)),
                            pygame.transform.scale(pygame.image.load("Images/fireball_2.png"),
                                                   (self.settings.fireball_width, self.settings.fireball_height)),
                            pygame.transform.scale(pygame.image.load("Images/fireball_3.png"),
                                                   (self.settings.fireball_width, self.settings.fireball_height)),
                            pygame.transform.scale(pygame.image.load("Images/fireball_4.png"),
                                                   (self.settings.fireball_width, self.settings.fireball_height))])
        self.explode_frames = []
        self.explode_frames.extend([pygame.transform.scale(pygame.image.load("Images/explode_0.png"),
                                                           (self.settings.fireball_width,
                                                            self.settings.fireball_height)),
                                    pygame.transform.scale(pygame.image.load("Images/explode_1.png"),
                                                           (self.settings.fireball_width,
                                                            self.settings.fireball_height)),
                                    pygame.transform.scale(pygame.image.load("Images/explode_2.png"),
                                                           (self.settings.fireball_width,
                                                            self.settings.fireball_height))])

        # Store location
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.fireball_speed = settings.fireball_speed

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, y, x):
        self.rect.top = y
        self.rect.left = x
        self.initial_pos = self.get_position()
        self.target_pos = (self.rect.x, self.rect.y - self.rect.h - 1)

    def set_max_jump_height(self):
        self.max_jump_height = self.rect.centery - self.settings.fireball_max_jump_height

    def mark_for_death(self):
        self.explode = True
        self.explosion_index = 0
        self.is_moving = False

    def check_off_screen(self):
        if self.rect.x < 0 or \
                self.rect.y > self.settings.screen_height or \
                self.rect.y < 0:
            self.kill()

    def update(self):
        self.check_off_screen()

        if self.explode:
            self.iterate_index(len(self.explode_frames))
            self.image = self.explode_frames[self.explosion_index]
        else:
            self.iterate_index(len(self.images))
            self.image = self.images[self.index]

        # Update Position
        if self.is_moving:
            if self.facing_left:
                self.rect.centerx -= self.settings.fireball_speed
            else:
                self.rect.centerx += self.settings.fireball_speed

            print('fb y_val: ' + str(self.rect.centery))
            if self.is_falling:
                self.rect.centery += self.settings.fireball_jump
            elif not self.is_falling and self.rect.centery < self.max_jump_height:
                self.is_falling = True
            elif not self.is_falling:
                self.rect.centery -= self.settings.fireball_jump

    def iterate_index(self, max):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 50:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
            if self.explode:
                self.explosion_index += 1

            # temporarily placed movement in iterate, should belong in its own function
            # if self.fall:
            #     self.rect.centery += self.settings.fireball_jump
            # else:
            #     self.rect.centery -= self.settings.fireball_jump
        if self.index == max:
            self.index = 0

        if self.explosion_index == len(self.explode_frames):
            self.explosion_index = 0
            if self.explode:
                self.kill()
            # self.fall = not self.fall
