
import pygame
from pygame.sprite import Sprite


class Coin(Sprite):
    def __init__(self, screen, settings):
        super(Coin, self).__init__()
        self.screen = screen
        self.settings = settings

        self.idle = True
        self.kill_flag = False
        self.index = 0
        self.last_tick = pygame.time.get_ticks()

        # Item states
        self.start_spawn = False
        self.facing_left = False
        self.is_moving = False

        self.image = pygame.transform.scale(pygame.image.load("Images/white.png"), (self.settings.coin_width, self.settings.coin_height))

        self.rect = self.image.get_rect()
        self.time_index = 0
        self.initial_pos = (self.rect.x, self.rect.y)
        self.target_pos = (self.rect.x, self.rect.y)
        self.max_height_movement = self.rect.top - (settings.coin_move_factor * self.rect.h)
        self.y_vel = settings.coin_initial__move_speed

        self.images_idle = []
        self.images_idle.append(pygame.transform.scale(pygame.image.load("Images/coin_idle1.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))
        self.images_idle.append(pygame.transform.scale(pygame.image.load("Images/coin_idle2.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))
        self.images_idle.append(pygame.transform.scale(pygame.image.load("Images/coin_idle3.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))
        self.images_idle.append(pygame.transform.scale(pygame.image.load("Images/coin_idle4.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))

        self.images_move = []
        self.images_move.append(pygame.transform.scale(pygame.image.load("Images/coin_move1.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))
        self.images_move.append(pygame.transform.scale(pygame.image.load("Images/coin_move2.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))
        self.images_move.append(pygame.transform.scale(pygame.image.load("Images/coin_move3.png"),
                                                       (self.settings.coin_width, self.settings.coin_height)))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.idle:
            self.iterate_index(len(self.images_idle))
            self.image = self.images_idle[self.index]
        else:
            self.iterate_index(len(self.images_move))
            self.image = self.images_move[self.index]
        # update movement
        # print('coin pos: ' + str(self.rect.x) + ', ' + str(self.rect.y))
        if self.start_spawn:
            if self.rect.y > self.max_height_movement and self.y_vel < 0:
                self.rect.y += (abs(self.y_vel) * -1)
            elif self.rect.y <= self.target_pos[1]:
                self.rect.y += (self.y_vel)
            else:
                self.rect.y = self.initial_pos[1]

            # adjust velocity
            if self.rect.y <= self.target_pos[1]:
                self.y_vel = self.y_vel + (self.settings.coin_gravity*self.time_index)
                # print('y coin velocity: ' + str(self.y_vel))
                self.time_index += 1
            else:
                self.rect.top = self.initial_pos[1]
                self.y_vel = self.settings.coin_initial__move_speed
                self.start_spawn = False
                self.kill_flag = True
        if self.kill_flag:
            self.kill()

    def spawn(self):
        self.start_spawn = True
        self.idle = False
        self.settings.score_holder += self.settings.point_values['coin']
        self.settings.coin_holder += 1

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, y, x ):
        self.rect.top = y
        self.rect.left = x
        self.initial_pos = self.get_position()
        self.target_pos = self.get_position()
        self.max_height_movement = self.rect.top - (self.settings.coin_move_factor * self.rect.h)

    def iterate_index(self, max):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index == max:
            self.index = 0
            # if not self.idle:
                # Kill coin (move animation used for coins generated from mystery boxes and multi hit bricks)
                # self.kill_flag = True  # in a separate function remove the sprite from all groups using Sprite.kill()
