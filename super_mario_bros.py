
import pygame
import sys
from pygame.sprite import Group

import game_functions as gf
import map_generator as map
from settings import Settings
from game_state import Game_State
from game_stats import Game_Stats
from text import Text
from mario import Mario
from flag import Flag


def run():
    # Initialization
    pygame.init()
    settings = Settings()
    state = Game_State()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Super Mario Bros")
    bg_color = settings.bg_color
    stats = Game_Stats(screen, settings)

    clock = pygame.time.Clock()

    mario = Mario(screen, settings, stats)

    pygame.mixer.music.load("Sounds/overworld.mp3")
    pygame.mixer.music.play(-1)

    # Groups
    map_group = Group()
    block_group = Group()
    floor_group = Group()
    pipe_group = Group()
    enemy_group = Group()
    powerup_group = Group()
    fireball_group = Group()
    dead_group = Group()

    map.generate_map(screen, settings, map_group, floor_group, pipe_group, block_group, enemy_group)
    f = Flag(screen, settings, 198 * settings.block_width, 13 * settings.block_height)
    f.add(map_group)

    pipesprites = pipe_group.sprites()

    timer = 0
    death_counter = 0

    # Game Loop
    while state.running:
        settings.reset_holders()
        clock.tick(settings.fps)

        # handle mario death
        if mario.is_dead and death_counter <= 240:
            # draw black screen
            if death_counter == 60:
                screen.fill(settings.bg_color)
                stats.lives -= 1
                if stats.lives < 0:
                    stats.init_base_values()
                    #display game over
                    game_over_label = Text(None, settings.TEXT_SIZE, "Game Over", settings.WHITE, 0, 0)
                    game_over_label.rect.center = (settings.screen_width/2, settings.screen_height/2)
                    game_over_label.draw(screen)
                else:
                    # display level
                    lvl_str = "World " + str(stats.world) + "-" + str(stats.level_num)
                    level_label = Text(None, settings.TEXT_SIZE, lvl_str, settings.WHITE, 0, 0)
                    level_label.rect.center = (settings.screen_width/2, settings.screen_height/2)
                    level_label.draw(screen)
                pygame.display.flip()
            death_counter += 1
            print(death_counter)
        elif mario.is_dead and death_counter > 240:
            # reset
            death_counter = 0
            mario.kill()
            mario = Mario(screen, settings, stats)
            map_group = Group()
            block_group = Group()
            floor_group = Group()
            pipe_group = Group()
            enemy_group = Group()
            powerup_group = Group()
            fireball_group = Group()
            dead_group = Group()
            pygame.mixer.music.play(-1)
            map.generate_map(screen, settings, map_group, floor_group, pipe_group, block_group, enemy_group)
            f = Flag(screen, settings, 198 * settings.block_width, 13 * settings.block_height)
            f.add(map_group)
            stats.new_level()

        # victory -> change level -> use death_counter to reset
        if mario.has_won and death_counter <= 300:
            # draw black screen
            if death_counter == 100:
                stats.level_num += 1
                screen.fill(settings.bg_color)
                # display level
                lvl_str = "World " + str(stats.world) + "-" + str(stats.level_num)
                level_label = Text(None, settings.TEXT_SIZE, lvl_str, settings.WHITE, 0, 0)
                level_label.rect.center = (settings.screen_width / 2, settings.screen_height / 2)
                level_label.draw(screen)
                coming_soon = Text(None, settings.TEXT_SIZE, "Coming Soon", settings.WHITE, 0, 0)
                coming_soon.rect.center = (settings.screen_width / 2, (settings.screen_height / 2)+settings.SPACER)
                coming_soon.draw(screen)
                pygame.display.flip()
            death_counter += 1
            print(death_counter)
        elif mario.has_won and death_counter > 300:
            # reset game
            death_counter = 0
            mario.kill()
            mario = Mario(screen, settings, stats)
            map_group = Group()
            block_group = Group()
            floor_group = Group()
            pipe_group = Group()
            enemy_group = Group()
            powerup_group = Group()
            fireball_group = Group()
            dead_group = Group()
            pygame.mixer.music.load("Sounds/overworld.mp3")
            pygame.mixer.music.play(-1)
            map.generate_map(screen, settings, map_group, floor_group, pipe_group, block_group, enemy_group)
            f = Flag(screen, settings, 198 * settings.block_width, 13 * settings.block_height)
            f.add(map_group)
            stats.new_level()

        # Game Play
        gf.check_events(state, mario, screen, settings, fireball_group, map_group)
        # Update here
        if not mario.is_dead and not mario.has_won:
            if timer < settings.fps:
                timer += 1
            else:
                timer = 0
                stats.decrement_time()

            gf.update(screen, settings, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group, fireball_group, dead_group, f)

            if stats.did_time_runout():
                mario.dead()
            if stats.time == 100:
                pygame.mixer.Sound('Sounds/time_warning.wav').play()


            # update game values
            stats.add_score(settings.score_manager)
            stats.add_coin(settings.coin_manager)
            if settings.one_up:
                stats.lives += 1
                settings.one_up = False
            # Display here
            stats.update()
            gf.update_screen(screen, settings, stats, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group, fireball_group, dead_group, f)
        # stats.draw()


    pygame.quit()
    sys.exit()


run()
