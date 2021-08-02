import pygame
import random
from config import Config
from classes import Explosion, Powerup, Spawn, Shield


def collide():
    # Проверка столкновений противников и меток появления
    hits = pygame.sprite.groupcollide(Config.new_enemies, Config.spawns, False, True)
    for hit in hits:
        hit.remove(Config.new_enemies)
        hit.add(Config.enemies)
        hit.add(Config.enemies_mode1)

    # Проверка столкновений пули противника и пули игрока
    hits = pygame.sprite.groupcollide(Config.player_bullets, Config.enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = pygame.sprite.groupcollide(Config.tiles, Config.player_bullets, False, False)
    for hit in hits:
        if hit.type == "STEEL":
            if hits[hit][0].strength == 2:
                hit.kill()
            hits[hit][0].kill() # убрать пулю
        if hit.type == "BRICK":
            hit.kill() # убрать элементы стены
            hits[hit][0].kill() # убрать пулю
            Config.graph.walls.remove((hit.rect.x, hit.rect.y)) # убрать элемент стены из графа
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            pass
        if hit.type == "ICE":
            pass

    # Проверка столкновений пули противника с элементом стены
    hits = pygame.sprite.groupcollide(Config.tiles, Config.enemy_bullets, False, False)
    for hit in hits:
        if hit.type == "STEEL":
            if hits[hit][0].strength == 2:
                hit.kill()
            hits[hit][0].kill() # убрать пулю
        if hit.type == "BRICK":
            hit.kill() # убрать элементы стены
            hits[hit][0].kill() # убрать пулю
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            pass
        if hit.type == "ICE":
            pass

    # Проверка столкновений пули противника с противником (дружественный огонь)
    hits = pygame.sprite.groupcollide(Config.enemies, Config.enemy_bullets, False, False)
    for enemy in hits:
        for bullet in hits[enemy]:
            if enemy.id != bullet.owner_id:
                bullet.kill()

    # Проверка столкновений пули и щита
    for shield in Config.shields:
        hits = pygame.sprite.spritecollide(Config.shield, Config.enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not Config.shield.alive():
        hits = pygame.sprite.spritecollide(Config.player, Config.enemy_bullets, True)
        for hit in hits:
            Config.last_player_hit_time = Config.now
            if Config.player.armor > 100:
                Config.player.armor -= 100
            elif Config.player.armor > 0:
                Config.player.life -= 100 - Config.player.armor
                Config.player.armor = 0
            elif Config.player.armor == 0:
                Config.player.life -= 100

            if Config.player.life > 0:
                try:
                    Config.hit_sound.play()
                except:
                    pass
            else:
                Explosion(hit.rect.center) 
                for enemy in Config.enemies:
                    if enemy.mode == 2:
                        enemy.change_mode(2, 1)
                    if enemy.mode == 3:
                        enemy.change_mode(3, 1)
                Config.player.hide()
                Config.player.lives -= 1
                Config.player.downgrade(Config.player.rect.center)
                try:
                    Config.explosion_sound.play()
                except:
                    pass

    # Проверка столкновений пули игрока и противника
    hits = pygame.sprite.groupcollide(Config.enemies, Config.player_bullets, False, True)
    for hit in hits:
        Config.hits_interval = Config.now - Config.last_enemy_hit_time
        Config.last_enemy_hit_time = Config.now

        if hits[hit][0].strength == 2:
            if hit.armor > 200:
                    hit.armor -= 200
            elif hit.armor > 100:
                hit.life -= 200 - hit.armor
                hit.armor = 0
            elif hit.armor <= 100:
                hit.armor = 0
                hit.life = 0
        
        if hits[hit][0].strength == 1:
            if hit.armor > 100:
                hit.armor -= 100
            elif hit.armor > 0:
                hit.life -= 100 - hit.armor
                hit.armor = 0
            elif hit.armor == 0:
                hit.life -= 100

        if hit.life > 0:
            try:
                Config.hit_sound.play()
            except:
                pass
        else:                       # Если противник убит
            Config.current_score = 100
            Config.current_score_centerx = hit.rect.centerx + 20
            Config.current_score_top = hit.rect.top + 20
            Config.current_enemy_count -= 1
            Config.remaining_enemy_count -= 1
            if Config.current_enemy_count == 2:
                Config.enemy_respawn_time = Config.now
            if Config.remaining_enemy_count >= 3:
                if Config.current_enemy_count == 2:
                    Spawn(Config.spawn_coordinates_x[Config.total_enemy_count]) 
                if Config.current_enemy_count == 1:
                    Spawn(Config.spawn_coordinates_x[Config.total_enemy_count + 1]) 
            Config.total_score += 100
            Explosion(hit.rect.center)
            hit.kill()  
            try:
                Config.explosion_sound.play()
            except:
                pass
            
            if random.random() > 0.8:
                Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    ice_count = 0
    hits = pygame.sprite.spritecollide(Config.player, Config.tiles, False)
    for tile in hits:
        if tile.type == "STEEL":
            Config.player.stop()
        if tile.type == "BRICK":
            Config.player.stop()
        if tile.type == "GRASS":
            pass
        if tile.type == "WATER":
            Config.player.stop()
        if tile.type == "ICE":
            ice_count += 1

    # Обработка поведения игрока на льду
    if len(hits) >= 4 and ice_count == len(hits):
        Config.player.speed = 6
        Config.player.moving_blocked = True
    if Config.player.speedx == 0 and Config.player.speedy == 0:
        Config.player.speed = 4
        Config.player.moving_blocked = False

    # Проверка отсутствия столкновений игрока с элементом стены "ICE"
    hits = pygame.sprite.spritecollide(Config.player, Config.tiles, False)
    if not hits:
            Config.player.speed = 4
            Config.player.moving_blocked = False

    # Проверка столкновений противника в режиме 1 с элементом стены
    hits = pygame.sprite.groupcollide(Config.enemies_mode1, Config.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "STEEL":
                enemy.stop()
                enemy.last_rotate = Config.now
                enemy.rotate()
                break
            if tile.type == "BRICK":
                enemy.stop()
                enemy.last_rotate = Config.now
                enemy.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                enemy.stop()
                enemy.last_rotate = Config.now
                enemy.rotate()
                break
            if tile.type == "ICE":
                print("Ice")
                enemy.speed = 4
                Config.enemies_on_ice.add(enemy)
                
    # !!!Проверка столкновений противника в режиме 2 с элементом стены
    hits = pygame.sprite.groupcollide(Config.enemies_mode2, Config.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "ICE":
                enemy.ice_count += 1
        if len(hits[enemy]) >= 4 and enemy.ice_count == len(hits[enemy]):
            enemy.speed = 4
            Config.enemies_on_ice.add(enemy)
        enemy.ice_count = 0
                 
    # !!!Проверка столкновений противника в режиме 3 с элементом стены
    hits = pygame.sprite.groupcollide(Config.enemies_mode3, Config.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "ICE":
                enemy.ice_count += 1
        if len(hits[enemy]) >= 4 and enemy.ice_count == len(hits[enemy]):
            enemy.speed = 4
            Config.enemies_on_ice.add(enemy)
        enemy.ice_count = 0

    # Проверка отсутствия столкновений противника с элементом стены "ICE"
    hits = pygame.sprite.groupcollide(Config.enemies_on_ice, Config.tiles, False, False)
    if not hits:
        for enemy in Config.enemies_on_ice:
            enemy.speed = 2
            Config.enemies_on_ice.remove(enemy)
    else:
        for enemy in hits:
            for tile in hits[enemy]:
                if tile.type == "ICE":
                    enemy.ice_count += 1
            if enemy.ice_count < 4:        
                enemy.speed = 2
                Config.enemies_on_ice.remove(enemy)
            enemy.ice_count = 0

    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(Config.player, Config.powerups, True)
    for hit in hits:
        Config.powerup_hit_time = Config.now
        Config.current_score = 100
        Config.current_score_centerx = hit.rect.centerx
        Config.current_score_top = hit.rect.top
        Config.total_score += 100
        try:
            Config.powerup_sound.play()
        except:
            pass
        if hit.type == "gun":
            if Config.enemies:
                Config.new_enemies_number = Config.remaining_enemy_count - Config.current_enemy_count # Количество противников,
                for enemy in Config.enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    Config.remaining_enemy_count -= 1
                Config.current_enemy_count = 0
                Config.enemy_respawn_time = Config.now
                if Config.new_enemies_number != 0:
                    Spawn(Config.spawn_coordinates_x[Config.total_enemy_count])
                    Config.new_enemies_number -= 1
        if hit.type == "shield":
            if Config.shield.alive():
                Config.shield.kill()
            Config.shield = Shield(Config.player.rect.center)
        if hit.type == "base":
            Config.base.upgrade_wall()
        if hit.type == "levelup":
            Config.player.upgrade(Config.player.rect.center, Config.player.direction)
        if hit.type == "life":
            Config.player.lives += 1
            if Config.player.lives >= 5:
                Config.player.lives = 5
                Config.player.life = 100
        if hit.type == "time":
            Config.frozen_time = True
            Config.freeze_time = Config.now
            for enemy in Config.enemies:
                enemy.frozen = True 

    # Проверка столкновений противника и игрока
    hits = pygame.sprite.spritecollide(Config.player, Config.enemies, False)
    for hit in hits:
        if hit.mode == 1: # Если режим противника №1
            Config.player.stop()
            hit.stop()
            hit.last_rotate = Config.now
            hit.reverse()
        if hit.mode == 2 or hit.mode == 3: # Если режим противника №2 или №3
            Config.player.hide()
            Config.player.lives -= 1
            Config.player.downgrade(Config.player.rect.center)
            Explosion(hit.rect.center)
            for enemy in Config.enemies:
                if enemy.mode == 2:
                    enemy.change_mode(2, 1)
                if enemy.mode == 3:
                    enemy.change_mode(3, 1)
            try:
                Config.explosion_sound.play()
            except:
                pass

    # Проверка столкновений противников в режиме 1 друг с другом
    for enemy in Config.enemies_mode1:
        enemy.remove(Config.enemies_mode1)
        hits = pygame.sprite.spritecollide(enemy, Config.enemies_mode1, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = Config.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = Config.now
                enemy.reverse()
    
        enemy.add(Config.enemies_mode1)

    # Проверка столкновений противников в режиме 1 с противниками в режиме 2
    hits = pygame.sprite.groupcollide(Config.enemies_mode1, Config.enemies_mode2, False, False)
    for enemy_1 in hits:
        enemy_1.stop()
        for enemy_2 in hits[enemy_1]:
            enemy_2.path_update_time = pygame.time.get_ticks()
            Config.graph.walls.append((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
            start = (enemy_2.graph_coordinate_x, enemy_2.graph_coordinate_y)
            goal = (Config.player.graph_coordinate_x, Config.player.graph_coordinate_y)
            enemy_2.update_path(start, goal)
            Config.graph.walls.remove((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
    
    # Проверка столкновений противников в режиме 1 с противниками в режиме 3
    hits = pygame.sprite.groupcollide(Config.enemies_mode1, Config.enemies_mode3, False, False)
    for enemy_1 in hits:
        enemy_1.stop()
        for enemy_3 in hits[enemy_1]:
            enemy_3.path_update_time = pygame.time.get_ticks()
            Config.graph.walls.append((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
            start = (enemy_3.graph_coordinate_x, enemy_3.graph_coordinate_y)
            enemy_3.path_to_base, enemy_3.goal = enemy_3.get_min_path_to_base()
            Config.graph.walls.remove((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(Config.player, Config.base):
        Config.player.stop()

    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(Config.base, Config.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = Config.now
        hit.rotate()

    # Проверка столкновений пулей игрока и противников с базой
    hits1 = pygame.sprite.spritecollide(Config.base, Config.player_bullets, True)
    hits2 = pygame.sprite.spritecollide(Config.base, Config.enemy_bullets, True)
    if hits1 or hits2:
        if not Config.base.destroyed:
            Explosion(Config.base.rect.center)
            Config.base.destroyed = True
            Config.base.destroyed_time = Config.now
            try:
                Config.game_over_sound.play()
            except:
                pass
            Config.game_over_string = "GAME OVER"
            Config.game_over_string_centerx = Config.base.rect.centerx
            Config.game_over_string_top = Config.base.rect.top
