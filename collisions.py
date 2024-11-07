import pygame
import random
from configuration import Configuratuion
from classes import Explosion, Powerup, Spawn, Shield


def collide():
    # Проверка столкновений противников и меток появления
    hits = pygame.sprite.groupcollide(Configuratuion.new_enemies, Configuratuion.spawns, False, True)
    for hit in hits:
        hit.remove(Configuratuion.new_enemies)
        hit.add(Configuratuion.enemies)
        hit.add(Configuratuion.enemies_mode1)

    # Проверка столкновений пули противника и пули игрока
    hits = pygame.sprite.groupcollide(Configuratuion.player_bullets, Configuratuion.enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = pygame.sprite.groupcollide(Configuratuion.tiles, Configuratuion.player_bullets, False, False)
    for hit in hits:
        if hit.type == "STEEL":
            if hits[hit][0].strength == 2:
                hit.kill()
            hits[hit][0].kill() # убрать пулю
        if hit.type == "BRICK":
            hit.kill() # убрать элементы стены
            hits[hit][0].kill() # убрать пулю
            Configuratuion.graph.walls.remove((hit.rect.x, hit.rect.y)) # убрать элемент стены из графа
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            pass
        if hit.type == "ICE":
            pass

    # Проверка столкновений пули противника с элементом стены
    hits = pygame.sprite.groupcollide(Configuratuion.tiles, Configuratuion.enemy_bullets, False, False)
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
    hits = pygame.sprite.groupcollide(Configuratuion.enemies, Configuratuion.enemy_bullets, False, False)
    for enemy in hits:
        for bullet in hits[enemy]:
            if enemy.id != bullet.owner_id:
                bullet.kill()

    # Проверка столкновений пули и щита
    for shield in Configuratuion.shields:
        hits = pygame.sprite.spritecollide(Configuratuion.shield, Configuratuion.enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not Configuratuion.shield.alive():
        hits = pygame.sprite.spritecollide(Configuratuion.player, Configuratuion.enemy_bullets, True)
        for hit in hits:
            Configuratuion.last_player_hit_time = Configuratuion.now
            if Configuratuion.player.armor > 100:
                Configuratuion.player.armor -= 100
            elif Configuratuion.player.armor > 0:
                Configuratuion.player.life -= 100 - Configuratuion.player.armor
                Configuratuion.player.armor = 0
            elif Configuratuion.player.armor == 0:
                Configuratuion.player.life -= 100

            if Configuratuion.player.life > 0:
                try:
                    Configuratuion.hit_sound.play()
                except:
                    pass
            else:
                Explosion(hit.rect.center) 
                for enemy in Configuratuion.enemies:
                    if enemy.mode == 2:
                        enemy.change_mode(2, 1)
                    if enemy.mode == 3:
                        enemy.change_mode(3, 1)
                Configuratuion.player.hide()
                Configuratuion.player.lives -= 1
                Configuratuion.player.downgrade(Configuratuion.player.rect.center)
                try:
                    Configuratuion.explosion_sound.play()
                except:
                    pass

    # Проверка столкновений пули игрока и противника
    hits = pygame.sprite.groupcollide(Configuratuion.enemies, Configuratuion.player_bullets, False, True)
    for hit in hits:
        Configuratuion.hits_interval = Configuratuion.now - Configuratuion.last_enemy_hit_time
        Configuratuion.last_enemy_hit_time = Configuratuion.now

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
                Configuratuion.hit_sound.play()
            except:
                pass
        else:                       # Если противник убит
            Configuratuion.current_score = 100
            Configuratuion.current_score_centerx = hit.rect.centerx + 20
            Configuratuion.current_score_top = hit.rect.top + 20
            Configuratuion.current_enemy_count -= 1
            Configuratuion.remaining_enemy_count -= 1
            if Configuratuion.current_enemy_count == 2:
                Configuratuion.enemy_respawn_time = Configuratuion.now
            if Configuratuion.remaining_enemy_count >= 3:
                if Configuratuion.current_enemy_count == 2:
                    Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count]) 
                if Configuratuion.current_enemy_count == 1:
                    Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count + 1]) 
            Configuratuion.total_score += 100
            Explosion(hit.rect.center)
            hit.kill()  
            try:
                Configuratuion.explosion_sound.play()
            except:
                pass
            
            if random.random() > 0.8:
                Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    ice_count = 0
    hits = pygame.sprite.spritecollide(Configuratuion.player, Configuratuion.tiles, False)
    for tile in hits:
        if tile.type == "STEEL":
            Configuratuion.player.stop()
        if tile.type == "BRICK":
            Configuratuion.player.stop()
        if tile.type == "GRASS":
            pass
        if tile.type == "WATER":
            Configuratuion.player.stop()
        if tile.type == "ICE":
            ice_count += 1

    # Обработка поведения игрока на льду
    if len(hits) >= 4 and ice_count == len(hits):
        Configuratuion.player.speed = 6
        Configuratuion.player.moving_blocked = True
    if Configuratuion.player.speedx == 0 and Configuratuion.player.speedy == 0:
        Configuratuion.player.speed = 4
        Configuratuion.player.moving_blocked = False

    # Проверка отсутствия столкновений игрока с элементом стены "ICE"
    hits = pygame.sprite.spritecollide(Configuratuion.player, Configuratuion.tiles, False)
    if not hits:
            Configuratuion.player.speed = 4
            Configuratuion.player.moving_blocked = False

    # Проверка столкновений противника в режиме 1 с элементом стены
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_mode1, Configuratuion.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "STEEL":
                enemy.stop()
                enemy.last_rotate = Configuratuion.now
                enemy.rotate()
                break
            if tile.type == "BRICK":
                enemy.stop()
                enemy.last_rotate = Configuratuion.now
                enemy.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                enemy.stop()
                enemy.last_rotate = Configuratuion.now
                enemy.rotate()
                break
            if tile.type == "ICE":
                enemy.speed = 4
                Configuratuion.enemies_on_ice.add(enemy)
                
    # !!!Проверка столкновений противника в режиме 2 с элементом стены
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_mode2, Configuratuion.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "ICE":
                enemy.ice_count += 1
        if len(hits[enemy]) >= 4 and enemy.ice_count == len(hits[enemy]):
            enemy.speed = 4
            Configuratuion.enemies_on_ice.add(enemy)
        enemy.ice_count = 0
                 
    # !!!Проверка столкновений противника в режиме 3 с элементом стены
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_mode3, Configuratuion.tiles, False, False)
    for enemy in hits:
        for tile in hits[enemy]:
            if tile.type == "ICE":
                enemy.ice_count += 1
        if len(hits[enemy]) >= 4 and enemy.ice_count == len(hits[enemy]):
            enemy.speed = 4
            Configuratuion.enemies_on_ice.add(enemy)
        enemy.ice_count = 0

    # Проверка отсутствия столкновений противника с элементом стены "ICE"
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_on_ice, Configuratuion.tiles, False, False)
    if not hits:
        for enemy in Configuratuion.enemies_on_ice:
            enemy.speed = 2
            Configuratuion.enemies_on_ice.remove(enemy)
    else:
        for enemy in hits:
            for tile in hits[enemy]:
                if tile.type == "ICE":
                    enemy.ice_count += 1
            if enemy.ice_count < 4:        
                enemy.speed = 2
                Configuratuion.enemies_on_ice.remove(enemy)
            enemy.ice_count = 0

    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(Configuratuion.player, Configuratuion.powerups, True)
    for hit in hits:
        Configuratuion.powerup_hit_time = Configuratuion.now
        Configuratuion.current_score = 100
        Configuratuion.current_score_centerx = hit.rect.centerx
        Configuratuion.current_score_top = hit.rect.top
        Configuratuion.total_score += 100
        try:
            Configuratuion.powerup_sound.play()
        except:
            pass
        if hit.type == "gun":
            if Configuratuion.enemies:
                Configuratuion.new_enemies_number = Configuratuion.remaining_enemy_count - Configuratuion.current_enemy_count # Количество противников,
                for enemy in Configuratuion.enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    Configuratuion.remaining_enemy_count -= 1
                Configuratuion.current_enemy_count = 0
                Configuratuion.enemy_respawn_time = Configuratuion.now
                if Configuratuion.new_enemies_number != 0:
                    Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])
                    Configuratuion.new_enemies_number -= 1
        if hit.type == "shield":
            if Configuratuion.shield.alive():
                Configuratuion.shield.kill()
            Configuratuion.shield = Shield(Configuratuion.player.rect.center)
        if hit.type == "base":
            Configuratuion.base.upgrade_wall()
        if hit.type == "levelup":
            Configuratuion.player.upgrade(Configuratuion.player.rect.center, Configuratuion.player.direction)
        if hit.type == "life":
            Configuratuion.player.lives += 1
            if Configuratuion.player.lives >= 5:
                Configuratuion.player.lives = 5
                Configuratuion.player.life = 100
        if hit.type == "time":
            Configuratuion.frozen_time = True
            Configuratuion.freeze_time = Configuratuion.now
            for enemy in Configuratuion.enemies:
                enemy.frozen = True 

    # Проверка столкновений противника и игрока
    hits = pygame.sprite.spritecollide(Configuratuion.player, Configuratuion.enemies, False)
    for hit in hits:
        if hit.mode == 1: # Если режим противника №1
            Configuratuion.player.stop()
            hit.stop()
            hit.last_rotate = Configuratuion.now
            hit.reverse()
        if hit.mode == 2 or hit.mode == 3: # Если режим противника №2 или №3
            Configuratuion.player.hide()
            Configuratuion.player.lives -= 1
            Configuratuion.player.downgrade(Configuratuion.player.rect.center)
            Explosion(hit.rect.center)
            for enemy in Configuratuion.enemies:
                if enemy.mode == 2:
                    enemy.change_mode(2, 1)
                if enemy.mode == 3:
                    enemy.change_mode(3, 1)
            try:
                Configuratuion.explosion_sound.play()
            except:
                pass

    # Проверка столкновений противников в режиме 1 друг с другом
    for enemy in Configuratuion.enemies_mode1:
        enemy.remove(Configuratuion.enemies_mode1)
        hits = pygame.sprite.spritecollide(enemy, Configuratuion.enemies_mode1, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = Configuratuion.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = Configuratuion.now
                enemy.reverse()
    
        enemy.add(Configuratuion.enemies_mode1)

    # Проверка столкновений противников в режиме 1 с противниками в режиме 2
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_mode1, Configuratuion.enemies_mode2, False, False)
    for enemy_1 in hits:
        enemy_1.stop()
        for enemy_2 in hits[enemy_1]:
            enemy_2.path_update_time = pygame.time.get_ticks()
            Configuratuion.graph.walls.append((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
            start = (enemy_2.graph_coordinate_x, enemy_2.graph_coordinate_y)
            goal = (Configuratuion.player.graph_coordinate_x, Configuratuion.player.graph_coordinate_y)
            enemy_2.update_path(start, goal)
            Configuratuion.graph.walls.remove((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
    
    # Проверка столкновений противников в режиме 1 с противниками в режиме 3
    hits = pygame.sprite.groupcollide(Configuratuion.enemies_mode1, Configuratuion.enemies_mode3, False, False)
    for enemy_1 in hits:
        enemy_1.stop()
        for enemy_3 in hits[enemy_1]:
            enemy_3.path_update_time = pygame.time.get_ticks()
            Configuratuion.graph.walls.append((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))
            start = (enemy_3.graph_coordinate_x, enemy_3.graph_coordinate_y)
            enemy_3.path_to_base, enemy_3.goal = enemy_3.get_min_path_to_base()
            Configuratuion.graph.walls.remove((enemy_1.graph_coordinate_x, enemy_1.graph_coordinate_y))

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(Configuratuion.player, Configuratuion.base):
        Configuratuion.player.stop()

    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(Configuratuion.base, Configuratuion.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = Configuratuion.now
        hit.rotate()

    # Проверка столкновений пулей игрока и противников с базой
    hits1 = pygame.sprite.spritecollide(Configuratuion.base, Configuratuion.player_bullets, True)
    hits2 = pygame.sprite.spritecollide(Configuratuion.base, Configuratuion.enemy_bullets, True)
    if hits1 or hits2:
        if not Configuratuion.base.destroyed:
            Explosion(Configuratuion.base.rect.center)
            Configuratuion.base.destroyed = True
            Configuratuion.base.destroyed_time = Configuratuion.now
            try:
                Configuratuion.game_over_sound.play()
            except:
                pass
            Configuratuion.game_over_string = "GAME OVER"
            Configuratuion.game_over_string_centerx = Configuratuion.base.rect.centerx
            Configuratuion.game_over_string_top = Configuratuion.base.rect.top
