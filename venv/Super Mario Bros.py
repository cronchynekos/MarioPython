import sys
import pygame
from settings import Settings
from mario import Mario
from enemies import Goomba
from map import Map
from brick import Block
from game_events import EventLoop
from scoreboard import Scoreboard
from game_stats import GameStats
from gameover import Gameover

class Game:
        def __init__(self):
            pygame.init()
            self.ai_settings = Settings()
            self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
            pygame.display.set_caption("Super Mario Bros Clone")
            self.mario_player = Mario(self.ai_settings, self.screen)
            self.map = Map(self.ai_settings, self.screen, mapfile='Levels/first_level.txt', blockfile='Images/block_tile.png')
            self.stats = GameStats()
            self.scoreboard = Scoreboard(self.ai_settings, self.screen, self.stats)
            self.clock = pygame.time.Clock()
            self.gameover = Gameover(self.ai_settings, self.screen, self.stats)

        def play(self):
            while True:
                while self.stats.lives > 0:
                    self.mario_player = Mario(self.ai_settings, self.screen)
                    self.map = Map(self.ai_settings, self.screen, mapfile='Levels/first_level.txt', blockfile='Images/block_tile.png')
                    eloop = EventLoop(self.ai_settings, self.screen, self.mario_player, self.map, self.stats, self.scoreboard, finished = False)
                    self.map.create_level()
                    while not eloop.finished:
                        eloop.update_events()
                        eloop.check_input_events()
                        eloop.update_screen()
                        self.clock.tick(60)
                        print(self.clock.get_fps())
                    self.stats.lives -= 1
                    self.stats.score = 0
                self.stats.reset_stats()
                if self.stats.win:
                    self.gameover.show_winover()
                    self.stats.final_score = 0
                    self.stats.win = False
                else:
                    self.gameover.show_gameover()
                pygame.time.wait(3000)


game = Game()
game.play()