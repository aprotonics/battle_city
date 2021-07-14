import pygame
import random


WIDTH = 650 # ширина игрового окна
HEIGHT = 650 # высота игрового окна


def collide_test():
    import battle_city

    # Проверка столкновений противников и spawns
    hits = pygame.sprite.groupcollide(battle_city.new_enemies, battle_city.spawns, False, True)
    for hit in hits:
        hit.remove(battle_city.new_enemies)
        hit.add(battle_city.enemies)

    # Проверка столкновений пули противника и пули игрока
    hits = pygame.sprite.groupcollide(battle_city.player_bullets, battle_city.enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = pygame.sprite.groupcollide(battle_city.tiles, battle_city.player_bullets, False, False)
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

    # Проверка столкновений пули противника с элементом стены
    hits = pygame.sprite.groupcollide(battle_city.tiles, battle_city.enemy_bullets, False, False)
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
    for shield in battle_city.shields:
        hits = pygame.sprite.spritecollide(battle_city.shield, battle_city.enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not battle_city.shield.alive():
        hits = pygame.sprite.spritecollide(battle_city.player, battle_city.enemy_bullets, True)
        for hit in hits:
            last_player_hit_time = battle_city.now
            if battle_city.player.armor > 100:
                battle_city.player.armor -= 100
            elif battle_city.player.armor > 0:
                battle_city.player.life -= 100 - battle_city.player.armor
                player.armor = 0
            elif battle_city.player.armor == 0:
                battle_city.player.life -= 100

            if battle_city.player.life > 0:
                try:
                    battle_city.hit_sound.play()
                except NameError:
                    pass
            else:
                explosion = battle_city.Explosion(hit.rect.center)
                battle_city.player.hide()
                battle_city.player.lives -= 1
                battle_city.player.downgrade(battle_city.player.rect.center)
                try:
                    battle_city.explosion_sound.play()
                except NameError:
                    pass

    # Проверка столкновений пули игрока и противника
    hits = pygame.sprite.groupcollide(battle_city.enemies, battle_city.player_bullets, False, True)
    for hit in hits:
        battle_city.hits_interval = battle_city.now - battle_city.last_enemy_hit_time
        battle_city.last_enemy_hit_time = battle_city.now

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
                battle_city.hit_sound.play()
            except NameError:
                pass
        else:                       # Если противник убит
            battle_city.current_score = 100
            battle_city.current_score_centerx = hit.rect.centerx + 20
            battle_city.current_score_top = hit.rect.top + 20
            battle_city.current_enemy_count -= 1
            battle_city.remaining_enemy_count -= 1
            if battle_city.current_enemy_count == 2:
                enemy_respawn_time = battle_city.now
            if battle_city.remaining_enemy_count >= 3:
                if battle_city.current_enemy_count == 2:
                    spawn = battle_city.Spawn(battle_city.spawn_centerxs[battle_city.total_enemy_count]) 
                if battle_city.current_enemy_count == 1:
                    spawn = battle_city.Spawn(battle_city.spawn_centerxs[battle_city.total_enemy_count + 1]) 
            battle_city.total_score += 100
            explosion = battle_city.Explosion(hit.rect.center)
            hit.kill()  
            try:
                battle_city.explosion_sound.play()
            except NameError:
                pass
            
            if random.random() > 0.8:
                powerup = battle_city.Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    hits = pygame.sprite.spritecollide(battle_city.player, battle_city.tiles, False)
    for hit in hits:
        if hit.type == "STEEL":
            battle_city.player.stop()
            break
        if hit.type == "BRICK":
            battle_city.player.stop()
            break
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            battle_city.player.stop()
            break
        if hit.type == "ICE":
            pass

    # Проверка столкновений противника с элементом стены
    hits = pygame.sprite.groupcollide(battle_city.enemies, battle_city.tiles, False, False)
    for hit in hits:
        for tile in hits[hit]:
            if tile.type == "STEEL":
                hit.stop()
                hit.last_rotate = battle_city.now
                hit.rotate()
                break
            if tile.type == "BRICK":
                hit.stop()
                hit.last_rotate = battle_city.now
                hit.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                hit.stop()
                hit.last_rotate = battle_city.now
                hit.rotate()
                break
            if tile.type == "ICE":
                pass

    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(battle_city.player, battle_city.powerups, True)
    for hit in hits:
        powerup_hit_time = battle_city.now
        current_score = 100
        current_score_centerx = hit.rect.centerx
        current_score_top = hit.rect.top
        battle_city.total_score += 100
        try:
            battle_city.powerup_sound.play()
        except NameError:
            pass
        if hit.type == "gun":
            if battle_city.enemies:
                new_enemies_number = battle_city.remaining_enemy_count - battle_city.current_enemy_count # Количество противников,
                for enemy in battle_city.enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    battle_city.remaining_enemy_count -= 1
                current_enemy_count = 0
                enemy_respawn_time = battle_city.now
                if new_enemies_number != 0:
                    spawn = battle_city.Spawn(battle_city.spawn_centerxs[battle_city.total_enemy_count])
                    new_enemies_number -= 1
        if hit.type == "shield":
            if battle_city.shield.alive():
                battle_city.shield.kill()
            battle_city.shield = battle_city.Shield(battle_city.player.rect.center)
        if hit.type == "base":
            battle_city.base.upgrade_wall()
        if hit.type == "levelup":
            battle_city.player.upgrade(battle_city.player.rect.center, battle_city.player.direction)
        if hit.type == "life":
            battle_city.player.lives += 1
            if battle_city.player.lives >= 5:
                player.lives = 5
                player.life = 100
        if hit.type == "time":
            frozen_time = True
            freeze_time = battle_city.now
            for enemy in battle_city.enemies:
                enemy.frozen = True 

    # Проверка столкновений противника и игрока
    hits = pygame.sprite.spritecollide(battle_city.player, battle_city.enemies, False)
    for hit in hits:
        battle_city.player.stop()
        hit.stop()
        hit.last_rotate = battle_city.now
        hit.reverse()

    # Проверка столкновений противников друг с другом
    for enemy in battle_city.enemies:
        enemy.remove(battle_city.enemies)        
        hits = pygame.sprite.spritecollide(enemy, battle_city.enemies, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = battle_city.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = battle_city.now
                enemy.reverse()            
            
        enemy.add(battle_city.enemies)

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(battle_city.player, battle_city.base):
        battle_city.player.stop()

    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(battle_city.base, battle_city.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = battle_city.now
        hit.rotate()

    # Проверка столкновений пули игрока и базы
    hits1 = pygame.sprite.spritecollide(battle_city.base, battle_city.player_bullets, True)

    # Проверка столкновений пули противников и базы
    hits2 = pygame.sprite.spritecollide(battle_city.base, battle_city.enemy_bullets, True)
    if hits1 or hits2:
        if not battle_city.base.destroyed:
            battle_city.explosion = battle_city.Explosion(battle_city.base.rect.center)
            battle_city.base.destroyed = True
            battle_city.base.destroyed_time = battle_city.now
            try:
                battle_city.game_over_sound.play()
            except NameError:
                pass
            battle_city.game_over_string = "GAME OVER"
            battle_city.game_over_string_centerx = battle_city.base.rect.centerx
            battle_city.game_over_string_top = battle_city.base.rect.top
