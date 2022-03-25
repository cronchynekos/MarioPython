import sys
import pygame
import time

class EventLoop:
    def __init__(self, ai_settings, screen, mario, map, stats, scoreboard, finished):
        self.finished = finished
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.mario = mario
        self.map = map
        self.stats = stats
        self.scoreboard = scoreboard
        self.carry_over = True

    def check_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            if self.mario.is_on_ground and not self.mario.is_dead:
                self.mario.velocity_y = -9.5
                self.mario.is_on_ground = False
                self.mario.is_jumping = True
        if event.key == pygame.K_LEFT:
            if not self.mario.is_along_wall and not self.mario.is_dead:
                self.mario.accel_x -= 0.125
                self.carry_over = False
        if event.key == pygame.K_RIGHT:
            if not self.mario.is_along_wall and not self.mario.is_dead:
                self.mario.accel_x += 0.125
                self.carry_over = False
        if event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_SPACE:
            if (self.mario.velocity_y < -1.0):
                self.mario.velocity_y = -1.0
        if event.key == pygame.K_LEFT:
            if not self.carry_over and not self.mario.is_dead:
                self.mario.accel_x += 0.125
        if event.key == pygame.K_RIGHT:
            if not self.carry_over and not self.mario.is_dead:
                self.mario.accel_x -= 0.125

    def update_events(self):
        if self.mario.rect.x > 780:
            self.finished = True
            self.stats.lives = 0
            self.stats.final_score = self.stats.score
            self.stats.win = True
        if self.mario.is_dead:
            self.mario.time_alive -= 1
            self.mario.velocity_x = 0
        self.map.update_map(self.mario, self.stats)
        self.mario.update(self.map)
        self.scoreboard.update_score()
        if self.mario.time_alive <= 0 and self.mario.rect.top:
            self.finished = True

    def update_screen(self):
        self.screen.fill(self.ai_settings.bg_color)
        self.map.draw_map()
        self.mario.draw_mario()
        self.scoreboard.show_score()
        pygame.display.flip()
