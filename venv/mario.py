import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet

class Mario:
    def __init__(self, ai_settings, screen):
        super(Mario, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.sprite = SpriteSheet('Images/mario.png')

        self.index = 0
        self.state = 0
        self.timer = 0

        self.image = self.sprite.image_get((32 * self.index, 32 * self.state, 32, 32))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.x = ai_settings.mario_width * 3
        self.rect.y = ai_settings.screen_height - ai_settings.mario_height * 9

        self.is_on_ground = False
        self.is_jumping = False
        self.is_along_wall = False
        self.is_dead = False

        self.time_alive = 120

        self.x = float(self.rect.x)

        self.velocity_y = 3.0
        self.velocity_x = 0.0
        self.accel_x = 0.0
        self.max_speed_x = 4
        self.max_speed_y = 8.0
        self.gravity = 0.3

        self.color = (10, 10, 10)

    def update(self, map):
        if not self.is_dead:
            self.bottom_of_screen()


        if self.is_dead:
            self.state = 3
        elif not self.is_on_ground:
            self.state = 2
        elif abs(self.velocity_x) > 0:
            self.state = 1
        else:
            self.state = 0

        self.x += int(self.velocity_x)
        if self.accel_x == 0:
            self.velocity_x *= 0.9
        if abs(self.velocity_x) < 0.05:
            self.velocity_x = 0
        self.velocity_x += self.accel_x
        if not self.is_dead:
            self.side_of_blocks(map.blocks)
        if abs(self.velocity_x) >= self.max_speed_x:
            if not self.velocity_x == 0:
                self.velocity_x = (self.velocity_x / abs(self.velocity_x)) * self.max_speed_x
        if self.x < self.screen_rect.left:
            self.x = self.screen_rect.left
        self.rect.x = self.x
        if not self.is_dead:
            self.side_of_blocks(map.blocks)
        if self.is_jumping:
            self.is_jumping = False
        else:
            if not self.is_dead:
                self.collide_with_blocks(map.blocks)

        if not self.is_on_ground or self.is_dead:
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed_y:
                self.velocity_y = self.max_speed_y
            self.rect.y += int(self.velocity_y)
            if not self.is_dead:
                self.collide_with_blocks(map.blocks)

        if self.timer < 3:
            self.timer += 1
        else:
            self.index += 1
            if self.index >= 8:
                self.index = 0
            self.image = self.sprite.image_get((32 * self.index, 32 * self.state, 32, 32))
            self.timer = 0

    def draw_mario(self):
        if self.velocity_x < 0:
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def collide_with_blocks(self, blocks):
        for block in blocks:
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.bottom)) or block.rect.collidepoint((self.rect.right - 1, self.rect.bottom)) or block.rect.collidepoint((self.rect.left + 1, self.rect.bottom)):
                if self.velocity_y <= 0:
                    self.is_on_ground = False
                    return False
                self.rect.y = block.rect.y - self.rect.height
                self.velocity_y = 0
                self.is_on_ground = True
                return True
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.top)) or block.rect.collidepoint((self.rect.right - 1, self.rect.top)) or block.rect.collidepoint((self.rect.left + 1, self.rect.top)):
                self.rect.y = block.rect.y + block.rect.height
                if not self.velocity_y >= 0:
                    self.velocity_y = 0
                block.is_headbutt = True
                block.velocity_y = -3.5
        self.is_on_ground = False
        return False

    def side_of_blocks(self, blocks):
        for block in blocks:
            if (block.rect.collidepoint((self.rect.left, self.rect.top + 1)) or block.rect.collidepoint((self.rect.left, self.rect.top + (self.rect.height / 2))) or block.rect.collidepoint((self.rect.left, self.rect.bottom - 1))) and abs(self.velocity_x) > 0:
                self.x = block.rect.x + self.rect.width
                self.rect.x = int(self.x)
                self.velocity_x = 0
                self.is_along_wall = True
            if (block.rect.collidepoint((self.rect.right, self.rect.top + 1))  or block.rect.collidepoint((self.rect.right, self.rect.top + (self.rect.height / 2))) or block.rect.collidepoint((self.rect.right, self.rect.bottom - 1))) and self.velocity_x >= 0:
                self.x = block.rect.x - self.rect.width
                self.rect.x = int(self.x)
                self.velocity_x = 0
                self.is_along_wall = True
        self.is_along_wall = False

    def bottom_of_screen(self):
        if self.rect.bottom >= self.screen_rect.bottom:
            self.velocity_y = -4.0
            self.is_dead = True