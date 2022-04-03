
from os.path import abspath, dirname
from text import Text


class Settings:
    def __init__(self):
        self.BASE_PATH = abspath(dirname(__file__))
        self.SOUND_PATH = self.BASE_PATH + '/Sounds/'
        self.IMAGE_PATH = self.BASE_PATH + '/Images/'

        # Settings
        self.screen_width = 1280
        self.screen_height = 720
        self.image_scale = 3
        self.fps = 60
        self.bg_color = (0, 0, 0)
        # Text
        self.WHITE = (255, 255, 255)
        self.ALT_TEXT_SIZE = 20
        self.SPACER = 54
        self.TEXT_SIZE = 36

        # Manages Score
        self.score_manager = 0
        self.coin_manager = 0
        self.one_up = False

        # Point Dictionary
        # TODO - finish points list
        self.point_values = {
            "coin": 200,
            "fire-flower": 1000,
            "star": 1000,
            "mushroom": 1000,
            "one-up": 1000,
            "goomba": 100,
            "koopa": 200,
            "brick": 50,
            "flag-top": 5000,
            "flag-mid": 2000,
            "flag-bot": 100
        }

        # Player Settings
        self.sm_width = 16 * self.image_scale - 2
        self.sm_height = 16 * self.image_scale
        self.bm_width = 16 * self.image_scale - 2
        self.bm_height = 32 * self.image_scale

        self.mario_walk = 4 * self.image_scale
        self.mario_run = 6 * self.image_scale
        self.mario_jump = 8 * self.image_scale
        self.mario_max_jump_height = 4 * self.sm_height + 5

        # Star Settings
        self.star_width = 16 * self.image_scale
        self.star_height = 16 * self.image_scale
        self.star_speed = 3 * self.image_scale
        self.star_jump = 4 * self.image_scale
        self.star_max_jump_height = 2 * self.sm_height

        # Coin Settings
        self.coin_height = 16 * self.image_scale
        self.coin_width = 16 * self.image_scale
        self.coin_move_factor = 2
        self.coin_initial__move_speed = -32
        self.coin_gravity = 1.01

        # Flower and Fireball Settings
        self.fireball_width = 8 * self.image_scale
        self.fireball_height = 8 * self.image_scale
        self.fire_flower_width = 16 * self.image_scale
        self.fire_flower_height = 16 * self.image_scale

        self.fireball_speed = 6 * self.image_scale
        self.fireball_jump = 4 * self.image_scale
        self.fireball_max_jump_height = 0.75 * self.sm_height
        self.fireball_limit = 2
        self.fireball_sound = self.SOUND_PATH + 'fireball.wav'

        # Floor Settings
        self.floor_width = 16 * self.image_scale
        self.floor_height = 16 * self.image_scale
        self.floor_image = self.IMAGE_PATH + 'floor.png'
        self.floor_ug_image = self.IMAGE_PATH + 'floor_ug.png'

        # Brick Settings
        self.brick_width = 16 * self.image_scale
        self.brick_height = 16 * self.image_scale
        self.brick_image = self.IMAGE_PATH + 'brick.png'
        # number of block heights it should move up
        self.brick_move_factor = 0.5
        self.brick_gravity = 1.01
        self.brick_initial_move_speed = -15
        # Underground Brick Settings
        self.brick_ug_image = self.IMAGE_PATH + 'brick_ug.png'

        # Broken Brick
        self.brick_rubble_height = 8 * self.image_scale
        self.brick_rubble_width = 8 * self.image_scale
        self.brick_rubble_left = self.IMAGE_PATH + 'block_debris_left.png'
        self.brick_rubble_right = self.IMAGE_PATH + 'block_debris_right.png'
        self.brick_rubble_height_factor = 0.2
        self.break_brick_sound = self.SOUND_PATH + 'breakblock.wav'
        self.brick_rubble_image_TBF = 100  # TBF - time between frames

        # BlockStairs Settings
        self.block_stairs_image = self.IMAGE_PATH + 'block.png'

        # Block Settings
        self.block_width = 16 * self.image_scale
        self.block_height = 16 * self.image_scale
        self.block_empty_image = self.IMAGE_PATH + 'block_empty.png'

        # Block Sounds
        self.coin_block_sound = self.SOUND_PATH + 'coin.wav'

        # Mystery Block Settings
        self.mystery_block_height = 16 * self.image_scale
        self.mystery_block_width = 16 * self.image_scale
        self.mystery_block_TBF = 100
        self.mystery_block_images = [
            self.IMAGE_PATH + 'qbrick_u_1.png',
            self.IMAGE_PATH + 'qbrick_u_2.png',
            self.IMAGE_PATH + 'qbrick_u_3.png',
            self.IMAGE_PATH + 'qbrick_u_2.png'
        ]
        self.mystery_block_possible_items = {
            'MUSHROOM': 'mushroom',
            'FIRE_FLOWER': 'fire-flower',
            'COIN': 'coin',
            'ONE_UP': '1-up',
            'STAR': 'star',
            'NONE': ''
        }
        self.mystery_block_sound = self.SOUND_PATH + 'powerup_appears.wav'

        # Pipe Settings
        self.pipe_width_size_factor = 2
        self.pipe_width = 16 * self.image_scale * self.pipe_width_size_factor
        self.pipe_height = 16 * self.image_scale
        self.pipe_image = self.IMAGE_PATH + 'pipe.png'
        self.horiz_pipe_image = self.IMAGE_PATH + 'horiz_pipe.png'
        self.pipe_sound = self.SOUND_PATH + 'pipe_hit.wav'

        # Flag settings
        self.flag_width = 16 * self.image_scale
        self.flag_height = 154 * self.image_scale
        self.flag_speed = 2 * self.image_scale

        # Goomba settings
        self.goomba_width = 16 * self.image_scale
        self.goomba_height = 16 * self.image_scale
        self.goomba_speed = 1 * self.image_scale

        # Koopa settings
        self.koopa_width = 16 * self.image_scale
        self.koopa_height = 24 * self.image_scale
        self.koopa_speed = 1 * self.image_scale

        # Shell Settings
        self.shell_speed = 4 * self.image_scale

        # Mushroom Settings
        self.mushroom_width = 16 * self.image_scale
        self.mushroom_height = 16 * self.image_scale
        self.mushroom_speed = 1 * self.image_scale
        self.mushroom_img = self.IMAGE_PATH + 'mushroom.png'
        self.oneup_img = self.IMAGE_PATH + '1_up.png'

        # Physics Settings
        self.gravity = 4 * self.image_scale

        # Item Settings
        self.item_box_spawn_speed = 2 * self.image_scale

    def reset_holders(self):
        self.score_holder = 0
        self.coin_holder = 0
        self.one_up = False
