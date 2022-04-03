
import pygame
from pygame import image
from pygame import mixer
from pygame.sprite import Sprite


class Pipe(Sprite):
    def __init__(self, screen, settings, height_factor=2, destinationPoint=None, isHorizontal=False):
        super(Pipe, self).__init__()
        self.settings = settings
        self.screen = screen

        self.is_horizontal = isHorizontal
        self.height_factor = height_factor
        self.destination = destinationPoint

        self.sound = mixer.Sound(settings.pipe_sound)

        self.image = pygame.Surface([settings.pipe_width, settings.pipe_height * self.height_factor], pygame.SRCALPHA,
                                    32).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((255, 255, 255, 0))
        self.state = None
        self.collision_pts = self.get_collision_points()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def get_collision_points(self):
        self.collision_pts = {
            "topSide": [self.rect.topleft, self.rect.midtop, self.rect.topright],
            "rightSide": [self.rect.topright, self.rect.midright, self.rect.bottomright],
            "botSide": [self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright],
            "leftSide": [self.rect.topleft, self.rect.midleft, self.rect.bottomleft],
        }
        return self.collision_pts

    def set_position(self, top, left):
        self.rect.top = top * self.settings.pipe_height
        self.rect.left = left * self.settings.pipe_width / self.settings.pipe_width_size_factor

    def check_entered(self, mario):
        if not self.destination:
            return None

        pts = None
        collision_pts = {
            "topSide": [mario.rect.topleft, mario.rect.midtop, mario.rect.topright],
            "rightSide": [mario.rect.topright, mario.rect.midright, mario.rect.bottomright],
            "botSide": [mario.rect.botleft, mario.rect.midbottom, mario.rect.botright]
        }

        if (not self.is_horizontal) and mario.crouch:
            pts = collision_pts["botSide"]
        elif self.is_horizontal and (not mario.facing_left):
            pts = collision_pts["rightSide"]

        if pts:
            if self.rect.collidepoint(pts[0]) and self.rect.collidepoint(pts[1]) and self.rect.collidepoint(pts[2]):
                return self.destination
