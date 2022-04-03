
from pygame.sprite import Sprite
from pygame import image
from pygame import mixer

import pygame
from coin import Coin
from fire_flower import Fire_Flower
from mushroom import Mushroom
from star import Star


class Block(Sprite):
    INVISIBLE = 'invisible'
    UNDERGROUND = 'underground'
    COIN = 'coin'
    MYSTERY = 'mystery'

    def __init__(self, screen, settings, is_underground=False, is_stairs=False):
        super(Block, self).__init__()
        self.screen = screen
        self.settings = settings
        self.is_underground = is_underground
        self.last_tick = pygame.time.get_ticks()
        self.index = 0
        self.initial_image = None
        self.curr_item = None

        # Block States
        self.is_hittable = True
        self.is_broken = False
        self.is_moving = False
        self.break_sound = mixer.Sound(settings.break_brick_sound)
        self.has_item = False

        # initial block image
        if is_stairs:
            self.initial_image = pygame.transform.scale(
                image.load(settings.block_stairs_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )
            self.is_hittable = False
        elif is_underground:
            self.initial_image = pygame.transform.scale(
                image.load(settings.brick_ug_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )

        else:
            self.initial_image = pygame.transform.scale(
                image.load(settings.brick_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )

        self.image = self.initial_image
        self.rect = self.image.get_rect()

        # Block Movement Settings
        self.y_vel = settings.brick_initial_move_speed
        self.initial_pos = (self.rect.x, self.rect.y)
        self.max_height_movement = self.rect.top - (settings.brick_move_factor * self.rect.h)

        self.collision_pts = self.get_collision_points()

    def set_position(self, top, left):
        self.rect.top = top * self.settings.block_height
        self.rect.left = left * self.settings.block_width
        self.initial_pos = self.get_position()

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def get_collision_points(self):
        self.collision_pts = {
            "topSide": [self.rect.topleft, self.rect.midtop, self.rect.topright],
            "rightSide": [self.rect.topright, self.rect.midright, self.rect.bottomright],
            "botSide": [self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright],
            "leftSide": [self.rect.topleft, self.rect.midleft, self.rect.bottomleft],
        }
        return self.collision_pts

    # def collision_check(self, sprite_object):
    #     pass

    def get_spawned_item(self):
        pass

    def handle_bottom_collision(self, map_group, can_break_block=False):
        if self.is_hittable and not self.is_broken:
            if can_break_block:
                self.break_block(map_group=map_group, rubble_group=pygame.sprite.Group())
            else:
                self.is_moving = True


    def update(self):
        if self.is_moving:
            # TODO animate block
            if self.rect.y > self.max_height_movement and self.y_vel < 0:
                self.rect.y += (abs(self.y_vel) * -1)
            elif self.rect.y <= self.initial_pos[1]:
                self.rect.y += (self.y_vel)
            else:
                self.rect.y = self.initial_pos[1]

            # adjust velocity
            if self.rect.y <= self.initial_pos[1]:
                self.y_vel += (abs(self.y_vel) * self.settings.brick_gravity)
                # print('y velocity: ' + str(self.y_vel))
            else:
                self.rect.top = self.initial_pos[1]
                self.y_vel = self.settings.brick_initial_move_speed
                self.is_moving = False
        # pass

    def animate_block_movement(self):
        pass

    def animate_internal_object(self, sprite_object):
        # TODO animate internal object to move to top of block
        if sprite_object:
            print('TODO - get sprite_object rect and move block')
        pass

    def break_block(self, rubble_group, map_group):
        if self.is_hittable:
            self.is_broken = True
            base_y_speed= 10
            speeds = [(-15, base_y_speed), (-10, base_y_speed), (10, base_y_speed), (15, base_y_speed)]
            for speed in speeds:
                left = False
                if speed[0] < 0:
                    left = True
                rubble = BrickRubblePiece(self.screen, self.settings, is_left=left, pos=(self.rect.centerx, self.rect.centery), x_speed=speed[0], y_speed=speed[1] )
                rubble_group.add(rubble)
                map_group.add(rubble)
            self.break_sound.play()
            self.settings.score_manager = self.settings.point_values['brick']
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def iterate_index(self, max_index):
        time = pygame.time.get_ticks() - self.last_tick
        if time > 100:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index == max_index:
            self.index = 0


class BrickRubblePiece(Sprite):
    def __init__(self, screen, settings, is_left=True, pos=(0,0), x_speed=0, y_speed=0):
        super(BrickRubblePiece, self).__init__()
        self.screen = screen
        self.settings = settings
        self.f_index = 0
        self.image = None
        self.last_tick = pygame.time.get_ticks()
        self.frames_list = [self.image, self.image, self.image, self.image]
        self.image_left = pygame.transform.scale(
            image.load(settings.brick_rubble_left),
            (settings.brick_rubble_width,
            settings.brick_rubble_height)
        )
        self.image_right = pygame.transform.scale(
            image.load(settings.brick_rubble_right),
            (settings.brick_rubble_width,
            settings.brick_rubble_height)
        )

        if is_left:
            self.image = self.image_left
            self.frames_list[::2] = [self.image_left] * 2
            self.frames_list[1::2] = [self.image_right] * 2

        else:
            self.image = self.image_right
            self.frames_list[::2] = [self.image_left] * 2
            self.frames_list[1::2] = [self.image_right] * 2
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.max_height = self.rect.y - (self.rect.y * settings.brick_rubble_height_factor)
        self.hit_max_arc = False
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        # update image
        self.iterate_index(len(self.frames_list))
        self.image = self.frames_list[self.f_index]
        #update pos
        self.rect.x += self.x_speed
        if self.hit_max_arc == False and self.rect.y > self.max_height:
            self.rect.y -= self.y_speed
        else:
            if not self.hit_max_arc:
                self.hit_max_arc = True
            self.rect.y += self.y_speed

        if self.x_speed > 0:
            self.x_speed -= 1
        else:
            self.x_speed += 1
        if self.rect.y > self.screen.get_height():
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def iterate_index(self, max_index):
        time = pygame.time.get_ticks() - self.last_tick
        if time > self.settings.brick_rubble_image_TBF:
            self.f_index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.f_index == max_index:
            self.f_index = 0
            # self.kill()


class CoinBlock(Block):
    def __init__(self, screen, settings, coins=0, is_underground=False):
        super(CoinBlock, self).__init__(screen, settings, is_underground)
        self.num_coins_left = coins
        self.coins = []
        self.empty_image = pygame.transform.scale(
            image.load(settings.block_empty_image),
            (self.settings.block_width,
             self.settings.block_height)
        )
        self.init_coin_list()
        self.sound = mixer.Sound(settings.coin_block_sound)
        self.is_hittable = True if coins > 0 else False
        self.has_item = True if coins > 0 else False

    def set_empty(self):
        self.is_hittable = False
        self.image = self.empty_image

    def init_coin_list(self):
        for i in range(self.num_coins_left):
            self.coins.append(Coin(self.screen, self.settings))

    def update(self):
        # Adjust Position
        if self.is_moving:
            # TODO animate block
            if self.rect.y > self.max_height_movement and self.y_vel < 0:
                self.rect.y += (abs(self.y_vel) * -1)
            elif self.rect.y <= self.initial_pos[1]:
                self.rect.y += (self.y_vel)
            else:
                self.rect.y = self.initial_pos[1]

            # adjust velocity
            if self.rect.y <= self.initial_pos[1]:
                self.y_vel += (abs(self.y_vel) * self.settings.brick_gravity)
                # print('y velocity: ' + str(self.y_vel))
            else:
                self.rect.top = self.initial_pos[1]
                self.y_vel = self.settings.brick_initial_move_speed
                self.is_moving = False

    def break_block(self, rubble_group, map_group):
        print('coins remaining: ' + str(len(self.coins)))
        if len(self.coins) <= 0:
            super().break_block( rubble_group=rubble_group, map_group=map_group)

    def handle_bottom_collision(self, map_group, can_break_block=False):
        if self.is_hittable:
            # TODO - figure out if need to adjust collided object physics
            self.has_item = self.num_coins_left > 0
            # Check if coins
            if self.has_item:
                self.num_coins_left -= 1

                # Animate Coin Trigger
                # TODO call coin animation - Make sure coin animation plays points
                coin_obj = self.coins.pop()
                coin_obj.set_position(self.rect.top, self.rect.left)
                coin_obj.add(map_group)
                coin_obj.spawn()
                self.curr_item = coin_obj


                # Play Coin Sounds
                self.sound.play()

                # Animate box movement
                self.is_moving = True

            # Set coinblock to empty if no coins
            if self.num_coins_left <= 0:
                self.set_empty()

    def get_spawned_item(self):
        if self.has_item:
            self.has_item = False
            return self.curr_item



class MysteryBlock(Block):

    def __init__(self, screen, settings, stored_item='', is_invisible=False, is_underground=False):
        super(MysteryBlock, self).__init__(screen, settings, is_underground)
        self.empty_image = pygame.transform.scale(
            image.load(settings.block_empty_image),
            (self.settings.block_width,
             self.settings.block_height)
        )
        self.stored_item = stored_item
        self.images_idle = []
        for i in range(len(settings.mystery_block_images)):
            self.images_idle.append(pygame.transform.scale(
                pygame.image.load(settings.mystery_block_images[i]),
                (self.settings.mystery_block_width,
                 self.settings.mystery_block_height)
            ))

        self.is_empty = False
        self.index = 0
        self.tick_time_limit = settings.mystery_block_TBF

        if is_invisible:
            self.initial_image = pygame.Surface([settings.brick_width, settings.brick_height], pygame.SRCALPHA, 32).convert_alpha()
            # TODO - remove this fill statement for hidden block
            self.initial_image.fill((255, 255, 255, 0))
            length = len(self.images_idle)
            self.images_idle.clear()
            for i in range(length):
                self.images_idle.append(self.initial_image)

        if self.stored_item == self.settings.mystery_block_possible_items['COIN']:
            self.sound = mixer.Sound(settings.coin_block_sound)
        else:
            self.sound = mixer.Sound(settings.mystery_block_sound)
        self.image = self.images_idle[0]
        self.rect = self.image.get_rect()

    def update(self):
        if not self.is_empty:
            # update idle frames
            self.iterate_index(len(self.images_idle))
            self.image = self.images_idle[self.index]
        # Adjust Position
        if self.is_moving:
            # TODO animate block
            if self.rect.y > self.max_height_movement and self.y_vel < 0:
                self.rect.y += (abs(self.y_vel) * -1)
            elif self.rect.y <= self.initial_pos[1]:
                self.rect.y += (self.y_vel)
            else:
                self.rect.y = self.initial_pos[1]

            # adjust velocity
            if self.rect.y <= self.initial_pos[1]:
                self.y_vel += (abs(self.y_vel) * self.settings.brick_gravity)
                # print('y velocity: ' + str(self.y_vel))
            else:
                self.rect.top = self.initial_pos[1]
                self.y_vel = self.settings.brick_initial_move_speed
                self.is_moving = False

    def break_block(self, rubble_group, map_group):
        if self.is_empty:
            self.is_hittable = False

    def set_empty(self):
        self.stored_item = self.settings.mystery_block_possible_items['NONE']
        self.is_empty = True
        self.is_hittable = False
        self.image = self.empty_image

    def handle_bottom_collision(self, map_group, can_break_block=False):
        if self.is_hittable:
            # TODO - figure out if need to adjust collided object physics
            if not self.is_empty:
                # Animate Contained Sprite to Appear
                item = self.make_item_appear()
                if item:
                    item.set_position(self.rect.top, self.rect.left)
                    print('item added to xy: ' + str(item.get_position()))
                    item.add(map_group)
                    self.curr_item = item
                    self.has_item = True
                # Play Sounds
                self.sound.play()

                # start moving block
                self.is_moving = True

                # Change To Empty
                self.set_empty()
        # else:
        # if collides with bottom and empty, force mario back down

    def get_spawned_item(self):
        if self.has_item:
            self.has_item = False
            return self.curr_item

    def make_item_appear(self):
        # TODO: animate sprite to appear in if/else below
        #   Move sprite up until bottom of sprite is at top of block
        obj = None
        if self.stored_item == self.settings.mystery_block_possible_items['MUSHROOM']:
            print('Mushroom item appears!')
            obj = Mushroom(self.screen, self.settings)
            obj.spawn()

        elif self.stored_item == self.settings.mystery_block_possible_items['FIRE_FLOWER']:
            print('Flower item appears!')
            obj = Fire_Flower(self.screen, self.settings)
            obj.spawn()


        elif self.stored_item == self.settings.mystery_block_possible_items['COIN']:
            print('Coin item appears!')
            obj = Coin(self.screen, self.settings)
            obj.spawn()

        elif self.stored_item == self.settings.mystery_block_possible_items['ONE_UP']:
            print('1UP item appears!')
            obj = Mushroom(self.screen, self.settings, is_one_up=True)
            obj.spawn()

        elif self.stored_item == self.settings.mystery_block_possible_items['STAR']:
            print('Star item appears!')
            obj = Star(self.screen, self.settings)
            obj.spawn()

        else:
            # shouldn't be empty!
            print('WARNING - mystery block missing item')
        return obj
        # self.animate_internal_object(obj)

    def iterate_index(self, max_index):
        time = pygame.time.get_ticks() - self.last_tick
        if time > self.tick_time_limit:
            self.index += 1
            self.last_tick = pygame.time.get_ticks()
        if self.index == max_index:
            self.index = 0


class BrickMysteryBlock(MysteryBlock):
    def __init__(self, screen, settings, stored_item='', is_underground=False):
        super(BrickMysteryBlock, self).__init__(screen, settings, stored_item=stored_item, is_invisible=False, is_underground=is_underground)

        # initial block image
        if is_underground:
            self.initial_image = pygame.transform.scale(
                image.load(settings.brick_ug_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )
        else:
            self.initial_image = pygame.transform.scale(
                image.load(settings.brick_image),
                (self.settings.brick_width,
                 self.settings.brick_height)
            )

        self.images_idle.clear()
        self.images_idle = [self.initial_image]
        self.image = self.images_idle[0]
        self.rect = self.image.get_rect()

