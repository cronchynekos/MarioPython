
import pygame
from pygame.sprite import Sprite
from fireball import Fireball


class Mario(Sprite):
    def __init__(self, screen, settings, stats):
        super(Mario, self).__init__()
        self.settings = settings
        self.screen = screen
        self.stats = stats

        self.victory_count = 0

        # States: sm = 0 | bm = 1 | fm = 2 | smi = 3 | bmi = 4
        self.state = 0
        self.is_dead = False
        self.is_flag = False
        self.victory = False
        self.walk = False
        self.run = False
        self.jump = False
        self.crouch = False
        self.shrink = False
        self.grow = False
        self.fireball = False
        self.fire_flower = False
        self.facing_left = False
        self.move_right = False
        self.move_left = False
        self.iframes = False
        self.index = 0
        self.last_tick = pygame.time.get_ticks()
        self.once_tick = pygame.time.get_ticks()
        self.invincible_tick = pygame.time.get_ticks()
        self.star_tick = pygame.time.get_ticks()
        self.was_fire = False
        self.has_won = False

        # Mario collision Flags
        self.is_falling = True
        self.is_jumping = False
        self.hit_wall = False

        self.image = pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                    (self.settings.sm_width, self.settings.sm_height))

        self.rect = self.image.get_rect()
        self.x = self.settings.sm_width * 3
        self.y = self.settings.sm_height * 12

        self.display_rect = pygame.Rect(0, 0, self.settings.bm_width, self.settings.bm_height)

        # Images for Small Mario
        self.sm_idle = pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                              (self.settings.sm_width, self.settings.sm_height))
        self.sm_walk = []
        self.sm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_walk1.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.sm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_walk2.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.sm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_walk3.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))

        self.sm_jump = pygame.transform.scale(pygame.image.load("Images/mario_small_jump.png"),
                                              (self.settings.sm_width, self.settings.sm_height))

        self.sm_grow = []
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.sm_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))

        self.sm_dead = pygame.transform.scale(pygame.image.load("Images/mario_death.png"),
                                              (self.settings.sm_width, self.settings.sm_height))

        # Images for Big Mario
        self.bm_idle = pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                              (self.settings.bm_width, self.settings.bm_height))
        self.bm_walk = []
        self.bm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_walk1.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.bm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_walk2.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.bm_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_walk3.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))

        self.bm_jump = pygame.transform.scale(pygame.image.load("Images/mario_big_jump.png"),
                                              (self.settings.bm_width, self.settings.bm_height))

        self.bm_crouch = pygame.transform.scale(pygame.image.load("Images/mario_big_crouch.png"),
                                                (self.settings.bm_width, self.settings.bm_height))

        self.bm_shrink = []
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.bm_shrink.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))

        # Images for Fire Mario
        self.fm_idle = pygame.transform.scale(pygame.image.load("Images/fire_mario_idle.png"),
                                              (self.settings.bm_width, self.settings.bm_height))
        self.fm_walk = []
        self.fm_walk.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_walk1.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.fm_walk.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_walk2.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.fm_walk.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_walk3.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))

        self.fm_jump = pygame.transform.scale(pygame.image.load("Images/fire_mario_jump.png"),
                                              (self.settings.bm_width, self.settings.bm_height))

        # NEED UPDATE - need to look for a fire mario fireball throw image
        self.fm_throw_fb = pygame.transform.scale(pygame.image.load("Images/fire_mario_idle.png"),
                                                  (self.settings.bm_width, self.settings.bm_height))

        self.fm_crouch = pygame.transform.scale(pygame.image.load("Images/fire_mario_crouch.png"),
                                                (self.settings.bm_width, self.settings.bm_height))

        self.fm_shrink = []
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_idle.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit.png"),
                                                     (self.settings.bm_width, self.settings.bm_height)))
        self.fm_shrink.append(pygame.transform.scale(pygame.image.load("Images/fire_mario_hit_idle.png"),
                                                     (self.settings.sm_width, self.settings.sm_height)))

        # Images for Small Mario Invincible
        self.smi_walk = []
        self.smi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_walk1.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.smi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_walk2.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.smi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_walk3.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))

        self.smi_jump = []
        self.smi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_jump1.png"),
                                               (self.settings.sm_width, self.settings.sm_height)))
        self.smi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_jump2.png"),
                                                    (self.settings.sm_width, self.settings.sm_height)))
        self.smi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_small_invincible_jump3.png"),
                                                    (self.settings.sm_width, self.settings.sm_height)))

        self.smi_sparkle = []
        self.smi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/small_mario_invincible_1.png"),
                                                       (self.settings.sm_width, self.settings.sm_height)))
        self.smi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/small_mario_invincible_2.png"),
                                                       (self.settings.sm_width, self.settings.sm_height)))
        self.smi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/small_mario_invincible_3.png"),
                                                       (self.settings.sm_width, self.settings.sm_height)))
        self.smi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/small_mario_invincible_4.png"),
                                                       (self.settings.sm_width, self.settings.sm_height)))

        self.smi_grow = []
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_small_idle.png"),
                                                   (self.settings.sm_width, self.settings.sm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_hit.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))
        self.smi_grow.append(pygame.transform.scale(pygame.image.load("Images/mario_big_idle.png"),
                                                   (self.settings.bm_width, self.settings.bm_height)))

        # Images for Big Mario Invincible
        self.bmi_walk = []
        self.bmi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_walk1.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_walk2.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_walk.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_walk3.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))

        self.bmi_jump = []
        self.bmi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_jump1.png"),
                                               (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_jump2.png"),
                                                    (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_jump3.png"),
                                                    (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_jump4.png"),
                                                    (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_jump.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_jump5.png"),
                                                    (self.settings.bm_width, self.settings.bm_height)))

        self.bmi_crouch = []
        self.bmi_crouch.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_crouch1.png"),
                                                (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_crouch.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_crouch2.png"),
                                                      (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_crouch.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_crouch3.png"),
                                                      (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_crouch.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_crouch4.png"),
                                                      (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_crouch.append(pygame.transform.scale(pygame.image.load("Images/mario_big_invincible_crouch5.png"),
                                                      (self.settings.bm_width, self.settings.bm_height)))

        self.bmi_sparkle = []
        self.bmi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/big_mario_invincible_1.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/big_mario_invincible_2.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/big_mario_invincible_3.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/big_mario_invincible_4.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))
        self.bmi_sparkle.append(pygame.transform.scale(pygame.image.load("Images/big_mario_invincible_5.png"),
                                                       (self.settings.bm_width, self.settings.bm_height)))

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.facing_left, False), self.rect)

    def dead(self):
        self.is_dead = True
        self.image = self.sm_dead
        pygame.mixer.music.stop()
        if self.stats.lives == 0:
            pygame.mixer.Sound("Sounds/gameover.wav").play()
        else:
            pygame.mixer.Sound("Sounds/die.wav").play()

    def throw_fireball(self, screen, settings, fireball_group, map_group):
        if self.facing_left:
            f = Fireball(screen, settings, self.rect.left, self.rect.centery)
            f.facing_left = True
            f.add(map_group, fireball_group)
        else:
            f = Fireball(screen, settings, self.rect.right, self.rect.centery)
            f.facing_left = False
            f.add(map_group, fireball_group)
        self.fireball = False


    def update(self, map_group):
        if self.rect.bottom >= self.screen.get_rect().bottom:
            self.dead()
            return

        if self.is_flag:
            return

        if self.victory and not self.is_flag and self.victory_count < 30:
            self.move_right = True
            self.move_left = False
            self.crouch = False
            self.walk = True
            self.victory_count += 1
        elif self.victory and not self.is_flag:
            self.move_right = False
            self.walk = False
            self.has_won = True

        if self.iframes:
            time = pygame.time.get_ticks() - self.invincible_tick
            if time > 3000:
                self.iframes = False
        self.walk = False
        if not self.shrink and not self.grow:
            if self.move_right and not self.crouch:
                self.walk = True
                if self.hit_wall:
                    print('hitting a wall')
                elif self.x >= self.settings.screen_width / 2:
                    for e in map_group:
                        if self.run:
                            e.rect.x -= self.settings.mario_run
                        else:
                            e.rect.x -= self.settings.mario_walk
                else:
                    if self.run:
                        self.x += self.settings.mario_run
                    else:
                        self.x += self.settings.mario_walk
            elif self.move_left and not self.crouch and self.x > 0:
                self.walk = True
                if self.hit_wall:
                    print('hitting a wall')
                elif self.run:
                    self.x -= self.settings.mario_run
                else:
                    self.x -= self.settings.mario_walk

            if self.is_falling:
                self.y += self.settings.gravity
                self.jump = True

            if self.is_jumping:
                if self.y <= self.max_jump_height:
                    self.is_falling = True
                    self.is_jumping = False
                    self.y += self.settings.gravity
                else:
                    self.y -= self.settings.mario_jump
                    self.is_falling = False
                    self.jump = True

        if self.state == 0:
            if self.grow:
                self.iterate_once(len(self.sm_grow))
                temp = self.rect.copy()
                self.image = self.sm_grow[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.bottom = temp.bottom
            elif self.shrink:
                self.image = self.sm_dead
            elif self.jump:
                self.image = self.sm_jump
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.walk:
                self.iterate_index(len(self.sm_walk))
                self.image = self.sm_walk[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.image = self.sm_idle
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        elif self.state == 1:  #Big Mario
            if self.shrink:
                self.iterate_once(len(self.bm_shrink))
                temp = self.rect.copy()
                self.image = self.bm_shrink[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.bottom = temp.bottom
            elif self.jump:
                self.image = self.bm_jump
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.crouch:
                self.image = self.bm_crouch
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.walk:
                self.iterate_index(len(self.bm_walk))
                self.image = self.bm_walk[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.image = self.bm_idle
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        elif self.state == 2:  # Fire Mario
            if self.shrink:
                self.iterate_once(len(self.fm_shrink))
                temp = self.rect.copy()
                self.image = self.fm_shrink[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.bottom = temp.bottom
            elif self.fireball:
                self.image = self.fm_throw_fb
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                self.fireball = False
            elif self.jump:
                self.image = self.fm_jump
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.crouch:
                self.image = self.fm_crouch
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.walk:
                self.iterate_index(len(self.fm_walk))
                self.image = self.fm_walk[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.image = self.fm_idle
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        elif self.state == 3:  # Small Mario Invincible
            self.star_timer()
            if self.grow:  # On mushroom collision set index to 0
                self.iterate_once(len(self.smi_grow))
                temp = self.rect.copy()
                self.image = self.smi_grow[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.bottom = temp.bottom
            elif self.jump:
                self.iterate_index(len(self.smi_jump))
                self.image = self.smi_jump[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.walk:
                self.iterate_index(len(self.smi_walk))
                self.image = self.smi_walk[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.iterate_index(len(self.smi_sparkle))
                self.image = self.smi_sparkle[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        elif self.state == 4:  # Big Mario Invinicble
            self.star_timer()
            if self.jump:
                self.iterate_index(len(self.bmi_jump))
                self.image = self.bmi_jump[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.crouch:
                self.iterate_index(len(self.bmi_crouch))
                self.image = self.bmi_crouch[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            elif self.walk:
                self.iterate_index(len(self.bmi_walk))
                self.image = self.bmi_walk[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
            else:
                self.iterate_index(len(self.bmi_sparkle))
                self.image = self.bmi_sparkle[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
        else:  # reset state to default on error (This should never happen)
            self.state = 0
            self.walk = False
            self.jump = False
            self.crouch = False
            self.shrink = False
            self.grow = False
            self.fireball = False
            self.facing_left = False
            self.move_right = False
            self.move_left = False
            self.index = 0

    def set_max_jump_height(self):
        self.max_jump_height = self.rect.y - self.settings.mario_max_jump_height

    def use_idle_image(self):
        # States: sm = 0 | bm = 1 | fm = 2 | smi = 3 | bmi = 4
        if self.state == 0:
            self.image = self.sm_idle
        elif self.state == 1:
            self.image = self.bm_idle
        elif self.state == 2:
            self.image = self.fm_idle
        elif self.state == 3:
            self.image = self.smi_idle
        elif self.state == 4:
            self.image = self.bmi_idle
        else:
            print('impossible state')

    def iterate_index(self, max):
        if self.index >= max:
            self.index = 0
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index >= max:
            self.index = 0

    def iterate_once(self, max):
        time = pygame.time.get_ticks() - self.once_tick
        if time > 100:
            self.index += 1
            self.once_tick = pygame.time.get_ticks()
        if self.index == max:
            if self.shrink:
                self.state = 0
            if self.state == 0 and self.grow and self.fire_flower:
                self.state = 2
            elif self.state == 0 and self.grow and not self.fire_flower:
                self.state = 1
            elif self.state == 3 and self.grow:
                self.state = 4
            self.shrink = False
            self.grow = False
            self.fire_flower = False
            self.index = 0

    def star_timer(self):
        time = pygame.time.get_ticks() - self.star_tick
        if time > 10000:
            if self.state == 3:
                self.state = 0
            elif self.state == 4:
                print('was fire' + str(self.was_fire))
                if self.was_fire:
                    self.was_fire = False
                    self.state = 2
                else:
                    self.state = 1
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Sounds/overworld.mp3")
            pygame.mixer.music.play()
