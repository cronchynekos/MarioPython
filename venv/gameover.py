import pygame.font

class Gameover:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.font = pygame.font.SysFont(None, 200)
        self.font2 = pygame.font.SysFont(None, 100)
        self.text_color = (255, 255, 255)
        self.stats = stats

        self.gameover_text = "GAME OVER"
        self.gameover_text_image = self.font.render(self.gameover_text, True, self.text_color, (0, 0, 0))
        self.gameover_text_rect = self.gameover_text_image.get_rect()
        self.gameover_text_rect.center = self.screen_rect.center

        self.winover_text = "YOU WIN"
        self.winover_text_image = self.font.render(self.winover_text, True, self.text_color, (0, 0, 0))
        self.winover_text_rect = self.winover_text_image.get_rect()
        self.winover_text_rect.center = self.screen_rect.center

        self.final_score = "FINAL SCORE: " + str(self.stats.final_score)
        self.final_score_image = self.font2.render(self.final_score, True, self.text_color, (0, 0, 0))
        self.final_score_rect = self.final_score_image.get_rect()
        self.final_score_rect.center = self.screen_rect.center
        self.final_score_rect.y = self.winover_text_rect.y + 200


    def show_gameover(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.gameover_text_image, self.gameover_text_rect)
        pygame.display.flip()

    def show_winover(self):
        self.final_score = "FINAL SCORE: " + str(self.stats.final_score)
        self.final_score_image = self.font2.render(self.final_score, True, self.text_color, (0, 0, 0))
        self.final_score_rect = self.final_score_image.get_rect()
        self.final_score_rect.center = self.screen_rect.center
        self.final_score_rect.y = self.winover_text_rect.y + 200

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.winover_text_image, self.winover_text_rect)
        self.screen.blit(self.final_score_image, self.final_score_rect)
        pygame.display.flip()