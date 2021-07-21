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
                except NameError:
                    pass
            else:
                Explosion(hit.rect.center) 
                for enemy in Config.enemies:
                    enemy.change_mode(2, 1)
                Config.player.hide()
                Config.player.lives -= 1
                Config.player.downgrade(Config.player.rect.center)
                try:
                    Config.explosion_sound.play()
                except NameError:
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
            except NameError:
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
            except NameError:
                pass
            
            if random.random() > 0.8:
                Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    hits = pygame.sprite.spritecollide(Config.player, Config.tiles, False)
    for hit in hits:
        if hit.type == "STEEL":
            Config.player.stop()
            break
        if hit.type == "BRICK":
            Config.player.stop()
            break
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            Config.player.stop()
            break
        if hit.type == "ICE":
            pass

    # Проверка столкновений противника с элементом стены
    hits = pygame.sprite.groupcollide(Config.enemies, Config.tiles, False, False)
    for hit in hits:
        for tile in hits[hit]:
            if tile.type == "STEEL":
                hit.stop()
                hit.last_rotate = Config.now
                hit.rotate()
                break
            if tile.type == "BRICK":
                hit.stop()
                hit.last_rotate = Config.now
                hit.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                hit.stop()
                hit.last_rotate = Config.now
                hit.rotate()
                break
            if tile.type == "ICE":
                pass

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
        except NameError:
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
        Config.player.stop()
        hit.stop()
        hit.last_rotate = Config.now
        hit.reverse()

    # Проверка столкновений противников друг с другом
    for enemy in Config.enemies:
        enemy.remove(Config.enemies)        
        hits = pygame.sprite.spritecollide(enemy, Config.enemies, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = Config.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = Config.now
                enemy.reverse()            
            
        enemy.add(Config.enemies)

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(Config.player, Config.base):
        Config.player.stop()

    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(Config.base, Config.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = Config.now
        hit.rotate()

    # Проверка столкновений пули игрока и базы
    hits1 = pygame.sprite.spritecollide(Config.base, Config.player_bullets, True)

    # Проверка столкновений пули противников и базы
    hits2 = pygame.sprite.spritecollide(Config.base, Config.enemy_bullets, True)
    if hits1 or hits2:
        if not Config.base.destroyed:
            Explosion(Config.base.rect.center)
            Config.base.destroyed = True
            Config.base.destroyed_time = Config.now
            try:
                Config.game_over_sound.play()
            except NameError:
                pass
            Config.game_over_string = "GAME OVER"
            Config.game_over_string_centerx = Config.base.rect.centerx
            Config.game_over_string_top = Config.base.rect.top
