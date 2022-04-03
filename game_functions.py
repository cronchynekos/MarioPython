

import pygame
from star import Star


def check_events(state, mario, screen, settings, fireball_group, map_group):
    # Checks for mouse and keyboard inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.running = False
        elif event.type == pygame.KEYDOWN:
            check_keydown(state, event, mario, screen, settings, fireball_group, map_group)
        elif event.type == pygame.KEYUP:
            check_keyup(event, mario)


def check_keydown(state, event, mario, screen, settings, fireball_group, map_group):
    if event.key == pygame.K_ESCAPE:
        state.running = False

    if event.key == pygame.K_SPACE and mario.state == 2 and len(fireball_group) < settings.fireball_limit:
        mario.throw_fireball(screen, settings, fireball_group, map_group)
        mario.fireball = True
        pygame.mixer.Sound("Sounds/fireball.wav").play()

    # Mario movement events
    elif event.key == pygame.K_RIGHT:
        mario.facing_left = False
        mario.move_left = False
        mario.move_right = True

    elif event.key == pygame.K_LEFT:
        mario.facing_left = True
        mario.move_left = True
        mario.move_right = False

    if mario.is_dead:
        return

    if event.key == pygame.K_UP:
        # set max jump height from first time
        if mario.is_jumping == False and mario.is_falling == False:
            mario.set_max_jump_height()
            mario.is_jumping = True
            if mario.state == 0 or mario.state == 3:
                pygame.mixer.Sound("Sounds/jump-small.wav").play()
            else:
                pygame.mixer.Sound("Sounds/jump-super.wav").play()
        mario.jump = True
    elif event.key == pygame.K_DOWN:
        mario.crouch = True

    if event.key == pygame.K_LCTRL:
        mario.run = True


def check_keyup(event, mario):
    if event.key == pygame.K_RIGHT:
        mario.move_right = False
    elif event.key == pygame.K_LEFT:
        mario.move_left = False

    if event.key == pygame.K_UP:
        # mario.jump = False
        # mario.is_falling = True
        mario.is_jumping = False
    elif event.key == pygame.K_DOWN:
        mario.crouch = False

    if event.key == pygame.K_LCTRL:
        mario.run = False


def update_dead(dead_group):
    for e in dead_group:
        if pygame.time.get_ticks() - e.death_timer > 1000:
            e.kill()


def enemy_stomp(e, mario, map_group, enemy_group, fireball_group, dead_group):
    if e.name == "Koopa":
        pygame.mixer.Sound("Sounds/stomp.wav").play()
        # e.kill()
        e.dead(map_group, enemy_group, fireball_group)
    elif e.name == "Goomba":
        e.rect.y -= 12
        pygame.mixer.Sound("Sounds/stomp.wav").play()
        # e.kill()
        e.dead()
        e.add(map_group, dead_group)
    elif e.name == "Shell":
        if e.active:
            if mario.iframes:
                return
            mario.dead()
        else:
            pygame.mixer.Sound("Sounds/shell_kick.wav").play()
            e.active = True
            mario.iframes = True
            mario.invincible_tick = pygame.time.get_ticks()
            if mario.rect.left < e.rect.right:
                e.facing_left = False
            else:
                e.facing_left = True


def mario_flag_collide(mario, flag, settings):
    if pygame.sprite.collide_rect(mario, flag):
        settings.score_holder += settings.point_values['flag-mid']
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sounds/stage_clear.wav")
        pygame.mixer.music.play()
        flag.raise_flag = True
        mario.is_flag = True
        if flag.flag_rect.top == flag.rect.top + 24:
            mario.is_flag = False
            mario.victory = True


def mario_powerup_collide(mario, map_group, powerup_group, settings):
    mg = pygame.sprite.Group()
    mario.add(mg)
    collisions = pygame.sprite.groupcollide(powerup_group, mg, True, False)
    for c in collisions:
        if c.name == "One Up":
            pygame.mixer.Sound("Sounds/1-up.wav").play()
            settings.score_holder += settings.point_values['one-up']
            settings.one_up = True
        elif c.name == "Mushroom":
            pygame.mixer.Sound("Sounds/powerup.wav").play()
            settings.score_holder += settings.point_values['mushroom']
            mario.index = 0
            if mario.state == 2:
                return
            elif mario.state == 0:
                mario.grow = True
            elif mario.state == 3:
                mario.grow = True
        elif c.name == "Fire Flower":
            pygame.mixer.Sound("Sounds/powerup.wav").play()
            settings.score_holder += settings.point_values['fire-flower']
            mario.fire_flower = True
            mario.was_fire = True
            print('set to fire' + str(mario.was_fire))
            if mario.state == 0:
                mario.grow = True
            elif mario.state == 1:
                mario.state = 2
        elif c.name == "Star":
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Sounds/starman.mp3")
            settings.score_holder += settings.point_values['star']
            pygame.mixer.music.play(loops=-1)
            if mario.state == 0:
                mario.state = 3
            else:
                mario.state = 4
            mario.star_tick = pygame.time.get_ticks()
    mg.empty()


def collide_enemies(mario, map_group, enemy_group, fireball_group, dead_group):
    for f in fireball_group:
        if f.name == "Fireball":
            sprites = pygame.sprite.spritecollide(f, enemy_group, False)
            if sprites:
                f.mark_for_death()
                print(sprites)
                for s in sprites:
                    s.dead()
        else:
            for e in enemy_group:
                if e.name == "Shell":
                    continue
                else:
                    if pygame.sprite.collide_rect(e, f):
                        pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                        e.kill()

    for e in enemy_group:
        if pygame.sprite.collide_rect(mario, e):
            if mario.state == 0:
                if mario.is_falling:
                    enemy_stomp(e, mario, map_group, enemy_group, fireball_group, dead_group)
                else:
                    if e.name == "Shell":
                        if e.active:
                            if mario.iframes:
                                return
                            mario.dead()
                        else:
                            pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                            e.active = True
                            mario.iframes = True
                            mario.invincible_tick = pygame.time.get_ticks()
                            if mario.rect.left < e.rect.right:
                                e.facing_left = False
                            else:
                                e.facing_left = True
                    else:
                        if mario.iframes:
                            return
                        mario.dead()
            if mario.state == 1 and not mario.shrink:
                if mario.is_falling:
                    enemy_stomp(e, mario, map_group, enemy_group, fireball_group, dead_group)
                else:
                    if e.name == "Shell":
                        if e.active:
                            if mario.iframes:
                                return
                            mario.dead()
                        else:
                            pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                            e.active = True
                            mario.iframes = True
                            mario.invincible_tick = pygame.time.get_ticks()
                            if mario.rect.left < e.rect.right:
                                e.facing_left = False
                            else:
                                e.facing_left = True
                    else:
                        pygame.mixer.Sound("Sounds/shrink.wav").play()
                        mario.shrink = True
                        mario.once_tick = pygame.time.get_ticks()
                        mario.iframes = True
                        mario.invincible_tick = pygame.time.get_ticks()
                        mario.index = 0
            if mario.state == 2 and not mario.shrink:
                if mario.is_falling:
                    enemy_stomp(e, mario, map_group, enemy_group, fireball_group, dead_group)
                else:
                    if e.name == "Shell":
                        if e.active:
                            if mario.iframes:
                                return
                            mario.dead()
                        else:
                            pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                            e.active = True
                            mario.iframes = True
                            mario.invincible_tick = pygame.time.get_ticks()
                            if mario.rect.left < e.rect.right:
                                e.facing_left = False
                            else:
                                e.facing_left = True
                    else:
                        pygame.mixer.Sound("Sounds/shrink.wav").play()
                        mario.shrink = True
                        mario.once_tick = pygame.time.get_ticks()
                        mario.iframes = True
                        mario.invincible_tick = pygame.time.get_ticks()
                        mario.index = 0
            if mario.state == 3:
                pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                e.kill()
            if mario.state == 4:
                pygame.mixer.Sound("Sounds/shell_kick.wav").play()
                e.kill()


# item collides w/ top of block or pipe
def item_block_pipe_collide(item, block):
    if item.is_moving and item.is_falling:
        if (item.rect.bottom >= block.rect.top and
                ((block.rect.left <= item.rect.left <= block.rect.right) or
                 (block.rect.left <= item.rect.right <= block.rect.right)) and
                item.rect.top < block.rect.top):
            # print('item block collision detected')
            item.rect.top = block.rect.top - item.rect.h - 1
            item.is_falling = False
            item.set_max_jump_height()
            # TODO edit entity falling status if needed
            return True
    return False


def item_floor_collide(item, floor):
    if item.is_moving and item.is_falling:
        if (item.rect.bottom >= floor.rect.top and
                (floor.rect.left <= item.rect.centerx <= floor.rect.right) and
                item.rect.top < floor.rect.top):
            # print('item floor collision detected')
            item.rect.y = floor.rect.top - item.rect.h - 1
            item.is_falling = False
            item.set_max_jump_height()
            # TODO edit entity falling status if needed
        return True
    return False


def item_wall_collide(item, wall):
    if item.is_moving:
        if (item.rect.right >= wall.rect.left and
                (wall.rect.top < item.rect.centery < wall.rect.bottom) and item.rect.left < wall.rect.left
                and not item.facing_left):
            # print('collision w/ left side')
            # entity.rect.right = wall.rect.left - 1
            item.facing_left = not item.facing_left
            # TODO code to change entity direction
            return True
        elif (item.rect.left <= wall.rect.right and
              (wall.rect.top < item.rect.centery < wall.rect.bottom) and item.rect.right > wall.rect.right
              and item.facing_left):
            # print('collision w/ right side')
            # entity.rect.left = wall.rect.right + 1
            item.facing_left = not item.facing_left
            # TODO code to change entity direction
            return True
    return False


# Fireball stuff
def fb_block_pipe_collide(fb, block):
    if fb.name == "Fireball" and fb.is_moving and fb.is_falling:
        if (fb.rect.bottom >= block.rect.top > fb.rect.top and
                ((block.rect.left <= fb.rect.left <= block.rect.right) or
                 (block.rect.left <= fb.rect.right <= block.rect.right))):
            # print('item block collision detected')
            fb.rect.top = block.rect.top - fb.rect.h - 1
            fb.is_falling = False
            fb.set_max_jump_height()
            return True
    return False


def fb_floor_collide(fb, floor):
    if fb.name == "Fireball" and fb.is_moving and fb.is_falling:
        if (fb.rect.bottom >= floor.rect.top > fb.rect.top and
                (floor.rect.left <= fb.rect.centerx <= floor.rect.right)):
            # print('item floor collision detected')
            fb.rect.y = floor.rect.top - fb.rect.h - 1
            fb.is_falling = False
            fb.set_max_jump_height()
            # TODO edit entity falling status if needed
        return True
    return False


def fb_wall_collide(fb, wall):
    if fb.name == "Fireball" and fb.is_moving:
        if (fb.rect.right >= wall.rect.left > fb.rect.left and
                (wall.rect.top < fb.rect.centery < wall.rect.bottom)
                and not fb.facing_left):
            fb.mark_for_death()
            return True
        elif (fb.rect.left <= wall.rect.right < fb.rect.right and
              (wall.rect.top < fb.rect.centery < wall.rect.bottom)
              and fb.facing_left):
            fb.mark_for_death()
            return True
    return False


# entity collides w/ top of block or pipe
def entity_block_pipe_collide(entity, block):
    if (entity.rect.bottom >= block.rect.top and
            ((block.rect.left <= entity.rect.left <= block.rect.right) or
             (block.rect.left <= entity.rect.right <= block.rect.right)) and
            entity.rect.top < block.rect.bottom):
        entity.rect.bottom = block.rect.top - 1
        # TODO edit entity falling status if needed
        return True
    return False


def entity_floor_collide(entity, floor):
    if (entity.rect.bottom >= floor.rect.top and
            (floor.rect.left <= entity.rect.centerx <= floor.rect.right) and
            entity.rect.top < floor.rect.top):
        entity.rect.y = floor.rect.top - entity.rect.h
        # TODO edit entity falling status if needed
        return True
    return False


def entity_wall_collide(entity, wall):
    if (entity.rect.right >= wall.rect.left and
            (wall.rect.top < entity.rect.centery < wall.rect.bottom) and entity.rect.left < wall.rect.left
            and not entity.hit_wall and not entity.facing_left):
        # print('collision w/ left side')
        # entity.rect.right = wall.rect.left - 1
        entity.facing_left = not entity.facing_left
        # TODO code to change entity direction
        return True
    elif (entity.rect.left <= wall.rect.right and
          (wall.rect.top < entity.rect.centery < wall.rect.bottom) and entity.rect.right > wall.rect.right
          and not entity.hit_wall and entity.facing_left):
        # print('collision w/ right side')
        # entity.rect.left = wall.rect.right + 1
        entity.facing_left = not entity.facing_left
        # TODO code to change entity direction
        return True
    return False


def mario_block_collide(mario, block):
    if (mario.rect.bottom >= block.rect.top and
            ((block.rect.left <= mario.rect.left <= block.rect.right) or
             (block.rect.left <= mario.rect.right <= block.rect.right)) and
            mario.rect.top < block.rect.top):
        # print('mario landed on block')
        mario.rect.bottom = block.rect.top - 1
        mario.is_falling = False
        mario.jump = False
        return True
    return False


def mario_pipe_collide(mario, pipe):
    if (mario.rect.bottom >= pipe.rect.top and
            ((pipe.rect.left <= mario.rect.left <= pipe.rect.right) or
             (pipe.rect.left <= mario.rect.right <= pipe.rect.right)) and
            mario.rect.top < pipe.rect.bottom and not mario.is_jumping):
        # print('mario landed on pipe')
        mario.rect.bottom = pipe.rect.top - 1
        # mario.y = mario.rect.y
        mario.set_max_jump_height()
        mario.is_falling = False
        mario.jump = False
        return True
    return False


def mario_floor_collide(mario, floor):
    if (mario.rect.bottom >= floor.rect.top and
            (floor.rect.left <= mario.rect.centerx <= floor.rect.right) and
            mario.rect.top < floor.rect.top):
        # mario.rect.bottom = floor.rect.top - 1
        # print('mario landed on floor')
        mario.y = floor.rect.top - mario.rect.h

        mario.is_falling = False
        mario.jump = False
        return True
    return False


def mario_wall_collide(mario, wall):
    # left side of wall
    if (mario.rect.right >= wall.rect.left and
            (wall.rect.top <= mario.rect.centery <= wall.rect.bottom or
             wall.rect.topleft[1] <= mario.rect.topright[1] < wall.rect.bottomleft[1] or
             wall.rect.topleft[1] < mario.rect.bottomright[1] <= wall.rect.bottomleft[1]) and
            mario.rect.left < wall.rect.left
            and not mario.hit_wall):
        # print('collision w/ left side')
        mario.rect.x = wall.rect.left - mario.rect.w - 1
        mario.x = mario.rect.x
        # mario.rect.x = wall.rect.right + 1
        # mario.rect.right = wall.rect.left - 1
        mario.hit_wall = True
        if mario.victory == True:
            mario.display = False
        return True
    elif (mario.rect.left <= wall.rect.right and
          (wall.rect.top <= mario.rect.centery <= wall.rect.bottom or
           wall.rect.topright[1] <= mario.rect.topleft[1] < wall.rect.bottomright[1] or
           wall.rect.topright[1] < mario.rect.bottomleft[1] <= wall.rect.bottomright[
               1]) and mario.rect.right > wall.rect.right and not mario.hit_wall):
        # print('collision w/ right side')
        # print('mario falling ' + str(mario.is_falling))
        # print('wall tr: ' + str(wall.rect.topright) + 'br: ' + str(wall.rect.bottomright))
        # print('mario tl: ' + str(mario.rect.topleft))
        # print('wall tr: ' + str(wall.rect.topright) + 'br: ' + str(wall.rect.bottomright))
        # print('mario bl: ' + str(mario.rect.bottomleft))

        mario.rect.x = wall.rect.right + 1
        mario.x = mario.rect.x
        # mario.rect.left = wall.rect.right + 1
        mario.hit_wall = True
        return True
    return False


def mario_block_bottom_collide(mario, block):
    if (mario.rect.top <= block.rect.bottom and
            block.rect.left <= mario.rect.centerx <= block.rect.right and
            (block.rect.left <= mario.rect.left < block.rect.right or
             block.rect.left < mario.rect.right <= block.rect.right) and
            mario.rect.centery > block.rect.centery and mario.is_jumping):
        # mario.rect.y = block.rect.bottom + mario.rect.h
        mario.rect.top = block.rect.bottom + 1
        # print('collided bottom')
        mario.is_falling = True
        mario.is_jumping = False
        return True
    return False


def mario_block_collision(mario, floor_group, pipe_group, block_group, map_group, powerup_group):
    mg = pygame.sprite.Group(mario)

    # Check if Hit a wall
    mario.hit_wall = False

    block_wall_hits = pygame.sprite.groupcollide(mg, block_group, False, False, collided=mario_wall_collide)
    pipe_wall_hits = pygame.sprite.groupcollide(mg, pipe_group, False, False, collided=mario_wall_collide)
    if (block_wall_hits or pipe_wall_hits) and not mario.is_jumping:
        print('exited with wall')
        # if pipe_wall_hits:
        #     mario.use_idle_image()
        mario.is_falling = True
        # return

    floor_wall_hits = pygame.sprite.groupcollide(mg, floor_group, False, False, collided=mario_wall_collide)
    if floor_wall_hits:
        mg.empty()
        return

    # Bottom of Block Collision
    block_hits = pygame.sprite.groupcollide(mg, block_group, False, False, collided=mario_block_bottom_collide)
    if block_hits:
        for blocks in block_hits.values():
            for block in blocks:
                # print('collided to bottom of a block')
                if mario.state == 0 or mario.state == 3:
                    block.handle_bottom_collision(map_group=map_group)
                else:
                    block.handle_bottom_collision(map_group=map_group, can_break_block=True)
                if block.has_item:
                    # print('block has item and added to powerups')
                    # print('block position: ' + str(block.initial_pos))
                    # print('block position lr: ' + str(block.rect.left) + ', ' + str(block.rect.top))
                    item = block.get_spawned_item()
                    item.add(powerup_group)
                if block.is_broken:
                    print('block broke - TODO kill any object above it')
        mg.empty()
        return

    # LANDING ON LOGIC
    mario.is_falling = True
    floor_hits = pygame.sprite.groupcollide(mg, floor_group, False, False, collided=mario_floor_collide)
    if floor_hits:
        mg.empty()
        return

    if mario.is_falling:
        block_hits = pygame.sprite.groupcollide(mg, block_group, False, False, collided=mario_block_collide)
        if block_hits:
            # print('fell on block')
            mg.empty()
            return

        pipe_hits = pygame.sprite.groupcollide(mg, pipe_group, False, False, collided=mario_pipe_collide)
        if pipe_hits:
            # print('fell on pipe')
            mg.empty()
            return

    # Clear mario group so no duplication
    mg.empty()
    # END mario_block_collision()


def enemy_block_collision(enemy_group, floor_group, pipe_group, block_group, map_group):
    # TODO enable enemy collisions when needed
    if True:
        # Check for Wall Collision

        e_block_wall_hits = pygame.sprite.groupcollide(enemy_group, block_group, False, False,
                                                       collided=entity_wall_collide)
        e_pipe_wall_hits = pygame.sprite.groupcollide(enemy_group, pipe_group, False, False,
                                                      collided=entity_wall_collide)

        enemy_floor_wall_check = pygame.sprite.groupcollide(enemy_group, floor_group, False, False,
                                                            collided=entity_wall_collide)
        if enemy_floor_wall_check:
            return

        # LANDING Logic Check
        e_floor_hits = pygame.sprite.groupcollide(enemy_group, floor_group, False, False, collided=entity_floor_collide)

        e_block_hits = pygame.sprite.groupcollide(enemy_group, block_group, False, False,
                                                  collided=entity_block_pipe_collide)
        if e_block_hits or e_floor_hits:
            return

        e_pipe_hits = pygame.sprite.groupcollide(enemy_group, pipe_group, False, False,
                                                 collided=entity_block_pipe_collide)
        if e_pipe_hits:
            return
    # END entity_block_collision


def item_block_collision(item_group, floor_group, pipe_group, block_group, map_group):
    # TODO: Add some check for if item is moving
    list_len = len(item_group)
    if list_len > 0:
        # Wall Collisions

        i_block_wall_hits = pygame.sprite.groupcollide(item_group, block_group, False, False,
                                                       collided=item_wall_collide)
        i_pipe_wall_hits = pygame.sprite.groupcollide(item_group, pipe_group, False, False,
                                                      collided=item_wall_collide)

        item_floor_wall_check = pygame.sprite.groupcollide(item_group, floor_group, False, False,
                                                           collided=item_wall_collide)
        if item_floor_wall_check:
            return

        items = iter(item_group)
        for _ in range(list_len):
            item = next(items)
            if not isinstance(item, Star):
                item.is_falling = True

        # LANDING Logic Check
        i_floor_hits = pygame.sprite.groupcollide(item_group, floor_group, False, False, collided=item_floor_collide)
        # if i_floor_hits:
        #     return
        i_block_hits = pygame.sprite.groupcollide(item_group, block_group, False, False,
                                                  collided=item_block_pipe_collide)
        if i_block_hits or i_floor_hits:
            return
        i_pipe_hits = pygame.sprite.groupcollide(item_group, pipe_group, False, False,
                                                 collided=item_block_pipe_collide)
        if i_pipe_hits:
            return
    # end item collision check


def fireball_block_collision(fb_group, floor_group, pipe_group, block_group, map_group):
    group_len = len(fb_group)
    if group_len > 0:
        fb_block_wall_hits = pygame.sprite.groupcollide(fb_group, block_group, False, False,
                                                        collided=fb_wall_collide)
        fb_pipe_wall_hits = pygame.sprite.groupcollide(fb_group, pipe_group, False, False,
                                                       collided=fb_wall_collide)
        fb_floor_wall_check = pygame.sprite.groupcollide(fb_group, floor_group, False, False,
                                                           collided=fb_wall_collide)
        if fb_floor_wall_check:
            return


        # LANDING Logic Check
        fb_floor_hits = pygame.sprite.groupcollide(fb_group, floor_group, False, False,
                                                  collided=fb_floor_collide)
        # if i_floor_hits:
        #     return
        fb_block_hits = pygame.sprite.groupcollide(fb_group, block_group, False, False,
                                                  collided=fb_block_pipe_collide)
        # if fb_block_hits or fb_floor_hits:
        #     return
        fb_pipe_hits = pygame.sprite.groupcollide(fb_group, pipe_group, False, False,
                                                 collided=fb_block_pipe_collide)
        if fb_pipe_hits:
            return



def check_collisions(settings, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group,
                     fireball_group, dead_group, f):
    # mario environment collisions
    mario_flag_collide(mario, f, settings)
    mario_block_collision(mario, floor_group, pipe_group, block_group, map_group, powerup_group)
    mario_powerup_collide(mario, map_group, powerup_group, settings)
    # mario enemy collisions
    collide_enemies(mario, map_group, enemy_group, fireball_group, dead_group)
    fireball_block_collision(fireball_group, floor_group, pipe_group, block_group, map_group)
    # entity (enemies/items) environment collisions
    enemy_block_collision(enemy_group, floor_group, pipe_group, block_group, map_group)
    item_block_collision(powerup_group, floor_group, pipe_group, block_group, map_group)


def update(screen, settings, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group,
           fireball_group, dead_group, f):
    map_group.update()
    mario.update(map_group)
    check_collisions(settings, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group,
                     fireball_group, dead_group, f)
    update_dead(dead_group)


def update_screen(screen, settings, stats, mario, map_group, floor_group, pipe_group, block_group, enemy_group, powerup_group,
                  fireball_group, dead_group, f):
    screen.fill(settings.bg_color)
    map_group.draw(screen)
    stats.draw()
    f.draw_flag()
    mario.draw()
    pygame.display.flip()
