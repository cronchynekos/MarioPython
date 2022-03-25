class GameStats:
    def __init__(self):
        self.score = 0
        self.final_score = 0
        self.lives = 3
        self.win = False

    def reset_stats(self):
        self.score = 0
        self.lives = 3