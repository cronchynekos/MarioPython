import pygame
from text import Text


class Game_Stats:

    def __init__(self,screen, settings):
        self.y_spacer = 290
        self.settings = settings
        self.screen = screen

        # String objects
        self.World = None
        self.Scores = None
        self.Time = None
        self.Lives = None
        self.Coins = None

        # Strings for UI
        self.t_text = "TIME"
        self.s_text = "SCORE"
        self.c_text = "COINS"
        self.l_text = "LIVES"
        self.w_text = "WORLD"

        self.Lives_Val = None
        self.Scores_Val = None
        self.Time_Val = None
        self.Coins_Val = None
        self.World_Val = None

        self.score = 0
        self.coins = 0
        self.coin_counter = 0
        self.world = 1
        self.level_num = 1
        self.lives = 3
        self.time = 400

        self.render()
        self.update()

    def init_base_values(self):
        self.score = 0
        self.coins = 0
        self.coin_counter = 0
        self.world = 1
        self.level_num = 1
        self.lives = 3
        self.time = 400

    def new_level(self):
        self.coin_counter = 0
        self.level_num = 1
        self.world = 1
        self.time = 400

    def did_lives_runout(self):
        return self.lives <= 0

    def did_time_runout(self):
        return self.time <= 0

    def add_score(self, num):
        self.score += num

    def add_coin(self, num):
        self.coins += num
        self.coin_counter += num
        if self.coin_counter == 100:
            self.lives += 1
            self.coin_counter = 0

    def get_world_and_level(self):
        return str(self.world) + '-' + str(self.level_num)

    def decrement_time(self):
        self.time -= 1

    def update(self):
        y_position = (self.screen.get_height() / 2) - (self.y_spacer) - 20

        self.Scores_Val = Text(None, self.settings.TEXT_SIZE, str(self.score), self.settings.WHITE, xpos=0, ypos=y_position)
        self.Scores_Val.rect.centerx = self.Scores.rect.centerx

        self.Coins_Val = Text(None, self.settings.TEXT_SIZE, str(self.coins), self.settings.WHITE, xpos=0, ypos=y_position)
        self.Coins_Val.rect.centerx = self.Coins.rect.centerx

        self.World_Val = Text(None, self.settings.TEXT_SIZE, self.get_world_and_level(), self.settings.WHITE, xpos=0, ypos=y_position)
        self.World_Val.rect.centerx = self.World.rect.centerx

        self.Time_Val = Text(None, self.settings.TEXT_SIZE, str(self.time), self.settings.WHITE, xpos=0, ypos=y_position)
        self.Time_Val.rect.centerx = self.Time.rect.centerx

        self.Lives_Val = Text(None, self.settings.TEXT_SIZE, str(self.lives), self.settings.WHITE, xpos=0, ypos=y_position)
        self.Lives_Val.rect.centerx = self.Lives.rect.centerx

    def render(self):
        y_position = self.settings.SPACER - (self.settings.SPACER/2)

        # Render the Score Display
        self.Scores = Text(None, self.settings.TEXT_SIZE, self.s_text, self.settings.WHITE, xpos=self.settings.SPACER, ypos=y_position)
        sRect = self.Scores.rect

        # Render the Coins Display
        cx_pos = sRect.x + sRect.width + self.settings.SPACER
        self.Coins = Text(None, self.settings.TEXT_SIZE, self.c_text, self.settings.WHITE, xpos=cx_pos, ypos=y_position)
        cRect = self.Coins.rect

        # Render the World Display
        wx_pos = cRect.x + cRect.width + self.settings.SPACER
        self.World = Text(None, self.settings.TEXT_SIZE, self.w_text, self.settings.WHITE, xpos=wx_pos, ypos=y_position)
        wRect = self.World.rect

        # Render the Time Left Display
        tx_pos = wRect.x + wRect.width + self.settings.SPACER
        self.Time = Text(None, self.settings.TEXT_SIZE, self.t_text, self.settings.WHITE, xpos=tx_pos, ypos=y_position)
        tRect = self.Time.rect

        # Render the Lives Display
        lx_pos = tRect.x + tRect.width + self.settings.SPACER
        self.Lives = Text(None, self.settings.TEXT_SIZE, self.l_text, self.settings.WHITE, xpos=lx_pos, ypos=y_position)

    def draw(self):
        self.Coins.draw(self.screen)
        self.Scores.draw(self.screen)
        self.World.draw(self.screen)
        self.Time.draw(self.screen)
        self.Lives.draw(self.screen)
        self.Scores_Val.draw(self.screen)
        self.Time_Val.draw(self.screen)
        self.Lives_Val.draw(self.screen)
        self.World_Val.draw(self.screen)
        self.Coins_Val.draw(self.screen)

