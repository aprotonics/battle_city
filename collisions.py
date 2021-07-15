def collide():
    import random
    import main

    # Проверка столкновений противников и spawns
    hits = main.pygame.sprite.groupcollide(main.new_enemies, main.spawns, False, True)
    for hit in hits:
        hit.remove(main.new_enemies)
        hit.add(main.enemies)

    # Проверка столкновений пули противника и пули игрока
    hits = main.pygame.sprite.groupcollide(main.player_bullets, main.enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = main.pygame.sprite.groupcollide(main.tiles, main.player_bullets, False, False)
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
    hits = main.pygame.sprite.groupcollide(main.tiles, main.enemy_bullets, False, False)
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
    for shield in main.shields:
        hits = main.pygame.sprite.spritecollide(main.shield, main.enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not main.shield.alive():
        hits = main.pygame.sprite.spritecollide(main.player, main.enemy_bullets, True)
        for hit in hits:
            last_player_hit_time = main.now
            if main.player.armor > 100:
                main.player.armor -= 100
            elif main.player.armor > 0:
                main.player.life -= 100 - main.player.armor
                player.armor = 0
            elif main.player.armor == 0:
                main.player.life -= 100

            if main.player.life > 0:
                try:
                    main.hit_sound.play()
                except NameError:
                    pass
            else:
                main.Explosion(hit.rect.center)
                main.player.hide()
                main.player.lives -= 1
                main.player.downgrade(main.player.rect.center)
                try:
                    main.explosion_sound.play()
                except NameError:
                    pass

    # Проверка столкновений пули игрока и противника
    hits = main.pygame.sprite.groupcollide(main.enemies, main.player_bullets, False, True)
    for hit in hits:
        main.hits_interval = main.now - main.last_enemy_hit_time
        main.last_enemy_hit_time = main.now

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
                main.hit_sound.play()
            except NameError:
                pass
        else:                       # Если противник убит
            main.current_score = 100
            main.current_score_centerx = hit.rect.centerx + 20
            main.current_score_top = hit.rect.top + 20
            main.current_enemy_count -= 1
            main.remaining_enemy_count -= 1
            if main.current_enemy_count == 2:
                main.enemy_respawn_time = main.now
            if main.remaining_enemy_count >= 3:
                if main.current_enemy_count == 2:
                    main.Spawn(main.spawn_centerxs[main.total_enemy_count]) 
                if main.current_enemy_count == 1:
                   main.Spawn(main.spawn_centerxs[main.total_enemy_count + 1]) 
            main.total_score += 100
            main.Explosion(hit.rect.center)
            hit.kill()  
            try:
                main.explosion_sound.play()
            except NameError:
                pass
            
            if random.random() > 0.8:
                powerup = main.Powerup(hit.rect.center)     
    
    # Проверка столкновений игрока с элементом стены
    hits = main.pygame.sprite.spritecollide(main.player, main.tiles, False)
    for hit in hits:
        if hit.type == "STEEL":
            main.player.stop()
            break
        if hit.type == "BRICK":
            main.player.stop()
            break
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            main.player.stop()
            break
        if hit.type == "ICE":
            pass

    # Проверка столкновений противника с элементом стены
    hits = main.pygame.sprite.groupcollide(main.enemies, main.tiles, False, False)
    for hit in hits:
        for tile in hits[hit]:
            if tile.type == "STEEL":
                hit.stop()
                hit.last_rotate = main.now
                hit.rotate()
                break
            if tile.type == "BRICK":
                hit.stop()
                hit.last_rotate = main.now
                hit.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                hit.stop()
                hit.last_rotate = main.now
                hit.rotate()
                break
            if tile.type == "ICE":
                pass

    # Проверка столкновений игрока и улучшений
    hits = main.pygame.sprite.spritecollide(main.player, main.powerups, True)
    for hit in hits:
        powerup_hit_time = main.now
        current_score = 100
        current_score_centerx = hit.rect.centerx
        current_score_top = hit.rect.top
        main.total_score += 100
        try:
            main.powerup_sound.play()
        except NameError:
            pass
        if hit.type == "gun":
            if main.enemies:
                new_enemies_number = main.remaining_enemy_count - main.current_enemy_count # Количество противников,
                for enemy in main.enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    main.remaining_enemy_count -= 1
                current_enemy_count = 0
                main.enemy_respawn_time = main.now
                if new_enemies_number != 0:
                    main.Spawn(main.spawn_centerxs[main.total_enemy_count])
                    new_enemies_number -= 1
        if hit.type == "shield":
            if main.shield.alive():
                main.shield.kill()
            main.shield = main.Shield(main.player.rect.center)
        if hit.type == "base":
            main.base.upgrade_wall()
        if hit.type == "levelup":
            main.player.upgrade(main.player.rect.center, main.player.direction)
        if hit.type == "life":
            main.player.lives += 1
            if main.player.lives >= 5:
                player.lives = 5
                player.life = 100
        if hit.type == "time":
            frozen_time = True
            freeze_time = main.now
            for enemy in main.enemies:
                enemy.frozen = True 

    # Проверка столкновений противника и игрока
    hits = main.pygame.sprite.spritecollide(main.player, main.enemies, False)
    for hit in hits:
        main.player.stop()
        hit.stop()
        hit.last_rotate = main.now
        hit.reverse()

    # Проверка столкновений противников друг с другом
    for enemy in main.enemies:
        enemy.remove(main.enemies)        
        hits = main.pygame.sprite.spritecollide(enemy, main.enemies, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = main.now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = main.now
                enemy.reverse()            
            
        enemy.add(main.enemies)

    # Проверка столкновений игрока и базы
    if main.pygame.sprite.collide_rect(main.player, main.base):
        main.player.stop()

    # Проверка столкновений противников и базы
    hits = main.pygame.sprite.spritecollide(main.base, main.enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = main.now
        hit.rotate()

    # Проверка столкновений пули игрока и базы
    hits1 = main.pygame.sprite.spritecollide(main.base, main.player_bullets, True)

    # Проверка столкновений пули противников и базы
    hits2 = main.pygame.sprite.spritecollide(main.base, main.enemy_bullets, True)
    if hits1 or hits2:
        if not main.base.destroyed:
            main.Explosion(main.base.rect.center)
            main.base.destroyed = True
            main.base.destroyed_time = main.now
            try:
                main.game_over_sound.play()
            except NameError:
                pass
            main.game_over_string = "GAME OVER"
            main.game_over_string_centerx = main.base.rect.centerx
            main.game_over_string_top = main.base.rect.top
