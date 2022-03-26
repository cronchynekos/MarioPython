
import pygame
from pygame.sprite import Sprite
from floor import Floor
from pipe import Pipe
from block import Block, MysteryBlock, CoinBlock, BrickMysteryBlock
from goomba import Goomba
from koopa import Koopa
from flag import Flag


class BG(Sprite):
    def __init__(self, screen, settings):
        super(BG, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("Images/map_1_1.png")
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width * self.settings.image_scale
        self.rect.height = self.rect.height * self.settings.image_scale
        self.image = pygame.transform.scale(self.image,
                                            (self.rect.width, self.rect.height))

    def draw(self):
        self.screen.blit(self.image, self.rect)


def generate_floor(screen, settings, map_group, floor_group, pipe_group):
    for i in range(0, 69):
        # level 15 and 16
        f = Floor(screen, settings)
        f.rect.top = 13 * settings.floor_height
        f.rect.left = i * settings.floor_width
        fl = Floor(screen, settings)
        fl.rect.top = 14 * settings.floor_height
        fl.rect.left = i * settings.floor_width
        # print('floor top: ' + str(f.rect.top))
        # print('floor x,y: ' + str(f.rect.x) + ', ' + str(f.rect.y))
        f.add(map_group, floor_group)
        fl.add(map_group, floor_group)
    for i in range(71, 86):
        f = Floor(screen, settings)
        f.rect.top = 13 * settings.floor_height
        f.rect.left = i * settings.floor_width
        fl = Floor(screen, settings)
        fl.rect.top = 14 * settings.floor_height
        fl.rect.left = i * settings.floor_width
        f.add(map_group, floor_group)
        fl.add(map_group, floor_group)
    for i in range(89, 153):
        f = Floor(screen, settings)
        f.rect.top = 13 * settings.floor_height
        f.rect.left = i * settings.floor_width
        fl = Floor(screen, settings)
        fl.rect.top = 14 * settings.floor_height
        fl.rect.left = i * settings.floor_width
        f.add(map_group, floor_group)
        fl.add(map_group, floor_group)
    for i in range(155, 224):
        f = Floor(screen, settings)
        f.rect.top = 13 * settings.floor_height
        f.rect.left = i * settings.floor_width
        fl = Floor(screen, settings)
        fl.rect.top = 14 * settings.floor_height
        fl.rect.left = i * settings.floor_width
        f.add(map_group, floor_group)
        fl.add(map_group, floor_group)

    # Stairs
    stairs_arr = []
    # 135-138,12 block
    for i in range(134, 138):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(12, i)
        stairs_arr.append(b)
    # 136-138,11 block
    for i in range(135, 138):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(11, i)
        stairs_arr.append(b)
    # 137,10 block
    # 138,10 block
    for i in range(136, 138):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(10, i)
        stairs_arr.append(b)
    # 138,9  block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(9, 137)
    stairs_arr.append(b)

    # 141-144,12 block
    for i in range(140, 144):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(12, i)
        stairs_arr.append(b)

    # 141-143,11 block
    for i in range(140, 143):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(11, i)
        stairs_arr.append(b)
    # 141-142,10 block
    for i in range(140, 142):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(10, i)
        stairs_arr.append(b)
    # 141,9  block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(9, 140)
    stairs_arr.append(b)

    # 149,12 block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(12, 148)
    stairs_arr.append(b)

    # 150,12 block
    # 150,11 block
    for i in range(11, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 149)
        stairs_arr.append(b)
    # 151,12 block
    # 151,11 block
    # 151,10 block
    for i in range(10, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 150)
        stairs_arr.append(b)
    # 152,12 block
    # 152,11 block
    # 152,10 block
    # 152,9  block
    for i in range(9, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 151)
        stairs_arr.append(b)
    # 153,12 block
    # 153,11 block
    # 153,10 block
    # 153,9  block
    for i in range(9, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 152)
        stairs_arr.append(b)

    # 156,12 block
    # 156,11 block
    # 156,10 block
    # 156,9  block
    for i in range(9, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 155)
        stairs_arr.append(b)
    # 157,12 block
    # 157,11 block
    # 157,10 block
    for i in range(10, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 156)
        stairs_arr.append(b)
    # 158,12 block
    # 158,11 block
    for i in range(11, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 157)
        stairs_arr.append(b)
    # 159,12 block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(12, 158)
    stairs_arr.append(b)

    # 182,12 block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(12, 181)
    stairs_arr.append(b)
    # 183,12 block
    # 183,11 block
    for i in range(11, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 182)
        stairs_arr.append(b)
    # 184,12 block
    # 184,11 block
    # 184,10 block
    for i in range(10, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 183)
        stairs_arr.append(b)
    # 185,12 block
    # 185,11 block
    # 185,10 block
    # 185,9 block
    for i in range(9, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 184)
        stairs_arr.append(b)
    # 186,12 block
    # 186,11 block
    # 186,10 block
    # 186,9 block
    # 186,8 block
    for i in range(8, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 185)
        stairs_arr.append(b)
    # 187,12 block
    # 187,11 block
    # 187,10 block
    # 187,9 block
    # 187,8 block
    # 187,7 block
    for i in range(7, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 186)
        stairs_arr.append(b)
    # 188,12 block
    # 188,11 block
    # 188,10 block
    # 188,9 block
    # 188,8 block
    # 188,7 block
    # 188,6 block
    for i in range(6, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 187)
        stairs_arr.append(b)
    # 189,12 block
    # 189,11 block
    # 189,10 block
    # 189,9 block
    # 189,8 block
    # 189,7 block
    # 189,6 block
    # 189,5 block
    for i in range(5, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 188)
        stairs_arr.append(b)
    # 190,12 block
    # 190,11 block
    # 190,10 block
    # 190,9 block
    # 190,8 block
    # 190,7 block
    # 190,6 block
    # 190,5 block
    for i in range(5, 13):
        b = Block(screen, settings, is_stairs=True)
        b.set_position(i, 189)
        stairs_arr.append(b)
    #
    # 199,12 block
    b = Block(screen, settings, is_stairs=True)
    b.set_position(12, 198)
    stairs_arr.append(b)

    for s in stairs_arr:
        s.add(map_group, floor_group)

    # Overworld Pipes
    p = Pipe(screen, settings)
    p.set_position(11, 28)
    p.add(map_group, pipe_group)
    print('pipe x,y' + str(p.rect.x) + ', ' + str(p.rect.y))

    p = Pipe(screen, settings, height_factor=3)
    p.set_position(10, 38)
    p.add(map_group, pipe_group)

    p = Pipe(screen, settings, height_factor=4)
    p.set_position(9, 46)
    p.add(map_group, pipe_group)

    # 58,12 pipe
    p = Pipe(screen, settings, height_factor=4)
    p.set_position(9, 57)
    p.add(map_group, pipe_group)

    p = Pipe(screen, settings)
    p.set_position(11, 163)
    p.add(map_group, pipe_group)

    p = Pipe(screen, settings)
    p.set_position(11, 179)
    p.add(map_group, pipe_group)

    # TODO: Generate Underworld Floors and Pipes


def generate_blocks(screen, settings, map_group, block_group):
    block_arr = []
    # 17,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 16)
    block_arr.append(mb)

    # 21,9 brick
    b = Block(screen, settings)
    b.set_position(9, 20)
    block_arr.append(b)

    # 22,9 mystery block (mushroom)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['MUSHROOM'])
    mb.set_position(9, 21)
    block_arr.append(mb)

    # 23,9 brick
    b = Block(screen, settings)
    b.set_position(9, 22)
    block_arr.append(b)

    # 23,5 mystery block (fire flower)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['FIRE_FLOWER'])
    mb.set_position(5, 22)
    block_arr.append(mb)

    # 24,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 23)
    block_arr.append(mb)

    # 25,9 brick
    b = Block(screen, settings)
    b.set_position(9, 24)
    block_arr.append(b)

    # 65,8 hiddent block (1up shroom)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['ONE_UP'], is_invisible=True)
    mb.set_position(8, 64)
    block_arr.append(mb)

    # 78,9 brick
    b = Block(screen, settings)
    b.set_position(9, 77)
    block_arr.append(b)

    # 79,9 mysteryblock (mushroom)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['MUSHROOM'])
    mb.set_position(9, 78)
    block_arr.append(mb)

    # 80,9 brick
    b = Block(screen, settings)
    b.set_position(9, 79)
    block_arr.append(b)

    # 81-88,5 brick
    for i in range(80, 88):
        b = Block(screen, settings)
        b.set_position(5, i)
        block_arr.append(b)

    # 92-94,5 brick
    for i in range(91, 94):
        b = Block(screen, settings)
        b.set_position(5, i)
        block_arr.append(b)

    # 95,9 multi hit block
    cb = CoinBlock(screen, settings, coins=12)
    cb.set_position(9, 94)
    block_arr.append(cb)

    # 95,5 mysterblock (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(5, 94)
    block_arr.append(mb)

    # 101,9 brick
    b = Block(screen, settings)
    b.set_position(9, 100)
    block_arr.append(b)

    # 102,9 brick(star)
    bmb = BrickMysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['STAR'])
    bmb.set_position(9, 101)
    block_arr.append(bmb)

    # 107,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 106)
    block_arr.append(mb)

    # 110,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 109)
    block_arr.append(mb)

    # 110,5 mystery block (mushroom)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['MUSHROOM'])
    mb.set_position(5, 109)
    block_arr.append(mb)

    # 113,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 112)
    block_arr.append(mb)

    # 119,9 brick
    b = Block(screen, settings)
    b.set_position(9, 118)
    block_arr.append(b)

    # 122-124, 5 brick
    for i in range(121, 124):
        b = Block(screen, settings)
        b.set_position(5, i)
        block_arr.append(b)

    # 129,5 brick
    b = Block(screen, settings)
    b.set_position(5, 128)
    block_arr.append(b)

    # 130,9 brick
    b = Block(screen, settings)
    b.set_position(9, 129)
    block_arr.append(b)

    # 130,5 mysteryblock (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(5, 129)
    block_arr.append(mb)

    # 131,9, brick
    b = Block(screen, settings)
    b.set_position(9, 130)
    block_arr.append(b)

    # 131,5 mysteryblock (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(5, 130)
    block_arr.append(mb)

    # 132,5 brick
    b = Block(screen, settings)
    b.set_position(5, 131)
    block_arr.append(b)

    # 169,9 brick
    b = Block(screen, settings)
    b.set_position(9, 168)
    block_arr.append(b)
    # 170,9 brick
    b = Block(screen, settings)
    b.set_position(9, 169)
    block_arr.append(b)
    # 171,9 mystery block (coin)
    mb = MysteryBlock(screen, settings, stored_item=settings.mystery_block_possible_items['COIN'])
    mb.set_position(9, 170)
    block_arr.append(mb)
    # 172,9 brick
    b = Block(screen, settings)
    b.set_position(9, 171)
    block_arr.append(b)

    #205, 12, brick
    b = Block(screen, settings)
    b.set_position(12, 223)
    block_arr.append(b)

    for o in block_arr:
        o.add(map_group, block_group)


def generate_entities(screen, settings, map_group, enemy_group):
    entity_arr = []
    # # 23,12 goomba
    g = Goomba(screen, settings)
    g.x = 22 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 41,12 goomba
    g = Goomba(screen, settings)
    g.x = 40 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 52,12 goomba
    g = Goomba(screen, settings)
    g.x = 51 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 54,12 goomba
    g = Goomba(screen, settings)
    g.x = 53 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 81,4  goomba
    g = Goomba(screen, settings)
    g.x = 80 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 11)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 83,4  goomba
    g = Goomba(screen, settings)
    g.x = 82 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 11)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 98,12 goomba
    g = Goomba(screen, settings)
    g.x = 97 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 100,12 goomba
    g = Goomba(screen, settings)
    g.x = 99 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 108,12 koopa
    k = Koopa(screen, settings)
    k.x = 107 * settings.floor_width
    k.rect.x = k.x
    k.y = settings.screen_height - (settings.floor_height * 3.5)
    k.rect.y = k.y
    entity_arr.append(k)
    # # 115,12 goomba
    g = Goomba(screen, settings)
    g.x = 114 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 117,12 goomba
    g = Goomba(screen, settings)
    g.x = 116 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 125,12 goomba
    g = Goomba(screen, settings)
    g.x = 124 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 127,12 goomba
    g = Goomba(screen, settings)
    g.x = 126 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 130,12 goomba
    g = Goomba(screen, settings)
    g.x = 129 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 132,12 goomba
    g = Goomba(screen, settings)
    g.x = 131 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 175,12 goomba
    g = Goomba(screen, settings)
    g.x = 174 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    # # 177,12 goomba
    g = Goomba(screen, settings)
    g.x = 176 * settings.floor_width
    g.rect.x = g.x
    g.y = settings.screen_height - (settings.floor_height * 3)
    g.rect.y = g.y
    entity_arr.append(g)
    for i in entity_arr:
        i.add(map_group, enemy_group)


def generate_map(screen, settings, map_group, floor_group, pipe_group, block_group, enemy_group):
    bg = BG(screen, settings)
    bg.add(map_group)
    generate_floor(screen, settings, map_group, floor_group, pipe_group)
    generate_blocks(screen, settings, map_group, block_group)
    generate_entities(screen, settings, map_group, enemy_group)
