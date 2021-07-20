import pygame
import random
import config
from classes import Explosion, Powerup, Spawn, Shield


def collide():
    # Проверка столкновений противников и меток появления
    hits = pygame.sprite.groupcollide(config.new_enemies, config.spawns, False, True)
    for hit in hits:
        hit.remove(config.new_enemies)
        hit.add(config.enemies)

    # Проверка столкновений пули противника и пули игрока
    hits = pygame.sprite.groupcollide(config.player_bullets, config.enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = pygame.sprite.groupcollide(config.tiles, config.player_bullets, False, False)
    for hit in hits:
        if hit.type == "STEEL":
            if hits[hit][0].strength == 2:
                hit.kill()
            hits[hit][0].kill() # убрать пулю
        if hit.type == "BRICK":
            hit.kill() # убрать элементы стены
            hits[hit][0].kill() # убрать пулю
            config.graph.walls.remove((hit.rect.x, hit.rect.y)) # убрать элемент стены из графа
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            pass
        if hit.type == "ICE":
            pass

    # Проверка столкновений пули противника с элементом стены
    hits = pygame.sprite.groupcollide(config.tiles, config.enemy_bullets, False, False)
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

    # Проверка столкновений пули и щита
    for shield in config.shields:
        hits = pygame.sprite.spritecollide(config.shield, config.enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not config.shield.alive():
        hits = pygame.sprite.spritecollide(config.player, config.enemy_bullets, True)
        for hit in hits:
            config.last_player_hit_time = config.now
            if config.player.armor > 100:
                config.player.armor -= 100
            elif config.player.armor > 0:
                config.player.life -= 100 - config.player.armor
                config.player.armor = 0
            elif config.player.armor == 0:
                config.player.life -= 100

            if config.player.life > 0:
                try:
                    config.hit_sound.play()
                except NameError:
                    pass
            else:
                Explosion(hit.rect.center) 
                for enemy in config.enemies:
                    enemy.change_mode(2, 1)
                config.player.hide()
                config.player.lives -= 1
                config.player.downgrade(config.player.rect.center)
                try:
                    config.explosion_sound.play()
                except NameError:
                    pass

    # Проверка столкновений пули игрока и противника
    hits = pygame.sprite.groupcollide(config.enemies, config.player_bullets, False, True)
    for hit in hits:
        config.hits_interval = config.now - config.last_enemy_hit_time
        config.last_enemy_hit_time = config.now

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
                config.hit_sound.play()
            except NameError:
                pass
        else:                       # Если противник убит
            config.current_score = 100
            config.current_score_centerx = hit.rect.centerx + 20
            config.current_score_top = hit.rect.top + 20
            config.current_enemy_count -= 1
            config.remaining_enemy_count -= 1
            if config.current_enemy_count == 2:
                config.enemy_respawn_time = config.now
            if config.remaining_enemy_count >= 3:
                if config.current_enemy_count == 2:
                    Spawn(config.spawn_coordinates_x[config.total_enemy_count]) 
                if config.current_enemy_count == 1:
                    Spawn(config.spawn_coordinates_x[config.total_enemy_count + 1]) 
            config.total_score += 100
            Explosion(hit.rect.center)
            hit.kill()  
            try:
                config.explosion_sound.play()
            except NameError:
                pass
            
            if random.random() > 0.8:
                Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    hits = pygame.sprite.spritecollide(config.player, config.tiles, False)
    for hit in hits:
        if hit.type == "STEEL":
            config.player.stop()
            break
        if hit.type == "BRICK":
            config.player.stop()
            break
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            config.player.stop()
            break
        if hit.type == "ICE":
            pass

    # Проверка столкновений противника с элементом стены
    hits = pygame.sprite.groupcollide(config.enemies, config.tiles, False, False)
    for hit in hits:
        for tile in hits[hit]:
            if tile.type == "STEEL":
                hit.stop()
                hit.last_rotate = config.now
                hit.rotate()
                break
            if tile.type == "BRICK":
                hit.stop()
                hit.last_rotate = config.now
                hit.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                hit.stop()
                hit.last_rotate = config.now
                hit.rotate()
                break
            if tile.type == "ICE":
                pass

    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(config.player, config.powerups, True)
    for hit in hits:
        config.powerup_hit_time = config.now
        config.current_score = 100
        config.current_score_centerx = hit.rect.centerx
        config.current_score_top = hit.rect.top
        config.total_score += 100
        try:
            config.powerup_sound.play()
        except NameError:
            pass
        if hit.type == "gun":
            if config.enemies:
                config.new_enemies_number = config.remaining_enemy_count - config.current_enemy_count # Количество противников,
                for enemy in config.enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    config.remaining_enemy_count -= 1
                config.current_enemy_count = 0
                config.enemy_respawn_time = config.now
                if config.new_enemies_number != 0:
                    Spawn(config.spawn_coordinates_x[config.total_enemy_count])
                    config.new_enemies_number -= 1
        if hit.type == "shield":
            if config.shield.alive():
                config.shield.kill()
            config.shield = Shield(config.player.rect.center)
        if hit.type == "base":
            config.base.upgrade_wall()
        if hit.type == "levelup":
            config.player.upgrade(config.player.rect.center, config.player.direction)
        if hit.type == "life":
            config.player.lives += 1
            if config.player.lives >= 5:
                config.player.lives = 5
                config.player.life = 100
        if hit.type == "time":
            config.frozen_time = True
            config.freeze_time = config.now
            for enemy in config.enemies:
                enemy.frozen = True 

    # Проверка столкновений противника и игрока
    hits = pygame.sprite.spritecollide(config.player, config.enemies, False)
    for hit in hits:
        config.player.stop()
        hit.stop()
        hit.last_rotate = config.now
        hit.reverse()

    # Проверка столкновений противников друг с другом
    for enemy in config.enemies:
        enemy.remove(config.enemies)        
        hits = pygame.sprite.spritecollide(enemy, config.enemies, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = config.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = config.now
                enemy.reverse()            
            
        enemy.add(config.enemies)

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(config.player, config.base):
        config.player.stop()

    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(config.base, config.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = config.now
        hit.rotate()

    # Проверка столкновений пули игрока и базы
    hits1 = pygame.sprite.spritecollide(config.base, config.player_bullets, True)

    # Проверка столкновений пули противников и базы
    hits2 = pygame.sprite.spritecollide(config.base, config.enemy_bullets, True)
    if hits1 or hits2:
        if not config.base.destroyed:
            Explosion(config.base.rect.center)
            config.base.destroyed = True
            config.base.destroyed_time = config.now
            try:
                config.game_over_sound.play()
            except NameError:
                pass
            config.game_over_string = "GAME OVER"
            config.game_over_string_centerx = config.base.rect.centerx
            config.game_over_string_top = config.base.rect.top
