import pygame.font

class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)

        self.score_text = "SCORE"
        self.score_text_image = self.font.render(self.score_text, True, self.text_color, self.ai_settings.bg_color)
        self.score_text_rect = self.score_text_image.get_rect()
        self.score_text_rect.centerx = self.screen_rect.left + 128
        self.score_text_rect.top = self.screen_rect.top

        self.lives_text = "LIVES"
        self.lives_text_image = self.font.render(self.lives_text, True, self.text_color, self.ai_settings.bg_color)
        self.lives_text_rect = self.lives_text_image.get_rect()
        self.lives_text_rect.centerx = self.screen_rect.right - 128
        self.lives_text_rect.top = self.screen_rect.top

        self.score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.score_text_rect.centerx
        self.score_rect.top = self.screen_rect.top + 32

        self.lives_str = "{:,}".format(self.stats.lives)
        self.lives_image = self.font.render(self.lives_str, True, self.text_color, self.ai_settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.centerx = self.lives_text_rect.centerx
        self.lives_rect.top = self.screen_rect.top + 32

    def update_score(self):
        self.score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.score_text_rect.centerx
        self.score_rect.top = self.screen_rect.top + 32

        self.lives_str = "{:,}".format(self.stats.lives)
        self.lives_image = self.font.render(self.lives_str, True, self.text_color, self.ai_settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.centerx = self.lives_text_rect.centerx
        self.lives_rect.top = self.screen_rect.top + 32

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_text_image, self.score_text_rect)
        self.screen.blit(self.lives_text_image, self.lives_text_rect)
        self.screen.blit(self.lives_image, self.lives_rect)