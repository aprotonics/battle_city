import pygame
import random
import os
import sys
import math
import datetime
from configuration import Configuratuion
from characters.player import Player
from characters.mob import Enemy, NormalEnemy, FastEnemy, EnhancedEnemy, HeavyEnemy
from classes import Shield, Base, Tile, Spawn
import collisions
import render


def get_time():
    now = pygame.time.get_ticks()
    current_seconds = math.trunc((now - Configuratuion.start_time) / 1000)
    current_minutes = 0
    while current_seconds >= 60:
        current_minutes += 1
        current_seconds -= 60
    if current_seconds < 10:
        current_seconds = f"0{str(current_seconds)}"
    if current_minutes < 10:
        current_minutes = f"0{str(current_minutes)}"
    current_time = f"{str(current_minutes)}:{str(current_seconds)}"
    return current_time


def draw_text(surf, x, y, text, size, color=(255, 255, 255)):
    font = pygame.font.Font(Configuratuion.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_start_screen():
    Configuratuion.screen.fill(Configuratuion.BLACK)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 2, Configuratuion.HEIGHT / 4, "Battle City", 64)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 2, Configuratuion.HEIGHT / 2, "Arrow keys to move, Space to fire", 22)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 2, Configuratuion.HEIGHT * 3 / 4, "Press ENTER to begin", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        Configuratuion.clock.tick(Configuratuion.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False


def show_game_over_screen():
    Configuratuion.screen.fill(Configuratuion.BLACK)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 2, Configuratuion.HEIGHT / 2 - 70, "GAME OVER", 70)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 2, Configuratuion.HEIGHT * 3 / 4, "Press any key to continue", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        Configuratuion.clock.tick(Configuratuion.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# создаем игру и окно
pygame.init()
try:
    pygame.mixer.init() # для звука
    # pygame.mixer.quit()
except Exception:
    pass
Configuratuion.screen = pygame.display.set_mode((Configuratuion.WIDTH, Configuratuion.HEIGHT))
pygame.display.set_caption("Battle city")
Configuratuion.clock = pygame.time.Clock()
Configuratuion.font_name = pygame.font.match_font("Arial")


# Цикл игры
before_start = True
level_won = False
running = True
game_over = False
while running:
    if before_start: 
        show_start_screen()
        before_start = False
        Configuratuion.start_time = pygame.time.get_ticks()
        Configuratuion.enemy_respawn_time = Configuratuion.start_time
        Configuratuion.last_enemy_hit_time = Configuratuion.start_time
        Configuratuion.last_player_hit_time = Configuratuion.start_time
        Configuratuion.powerup_hit_time = Configuratuion.start_time
        try:
            Configuratuion.game_start_sound.play()
        except:
            pass
        Configuratuion.all_sprites = pygame.sprite.Group()
        Configuratuion.enemies = pygame.sprite.Group()
        Configuratuion.new_enemies = pygame.sprite.Group()
        Configuratuion.enemies_on_ice = pygame.sprite.Group()
        Configuratuion.enemies_mode1 = pygame.sprite.Group()
        Configuratuion.enemies_mode2 = pygame.sprite.Group()
        Configuratuion.enemies_mode3 = pygame.sprite.Group()
        Configuratuion.bullets = pygame.sprite.Group()
        Configuratuion.player_bullets = pygame.sprite.Group()
        Configuratuion.enemy_bullets = pygame.sprite.Group()
        Configuratuion.powerups = pygame.sprite.Group()
        Configuratuion.tiles = pygame.sprite.Group()
        Configuratuion.spawns = pygame.sprite.Group()
        Configuratuion.shields = pygame.sprite.Group()
        Configuratuion.layers = pygame.sprite.LayeredUpdates()
        
        Configuratuion.player = Player(Configuratuion.player_image)
        Configuratuion.shield = Shield(Configuratuion.player.rect.center)     
        Configuratuion.base = Base()
        
        Configuratuion.current_score = ""
        Configuratuion.current_score_centerx = -100
        Configuratuion.current_score_top = -100
        Configuratuion.level_number = 1
        Configuratuion.total_score = 0
        Configuratuion.total_enemy = 5         # Количество противников на весь уровень
        Configuratuion.remaining_enemy_count = Configuratuion.total_enemy # Оставшееся количество противников
        Configuratuion.current_enemy_count = 0 # Текущее количество противников на карте
        Configuratuion.total_enemy_count = 0 # Общее количество появившихся противников
        Configuratuion.new_enemies_number = 0 # Количество противников, которое нужно добавить после применения улучшения Gun
        Configuratuion.hits_interval = 0
        Configuratuion.base_shield_start_time = 0
        Configuratuion.base_shield = False
        Configuratuion.freeze_time = 0
        Configuratuion.frozen_time = False
        
        Configuratuion.game_over_string = ""
        Configuratuion.game_over_string_centerx = -100
        Configuratuion.game_over_string_top = -100

        # Создание стен
        s = Configuratuion.TILE_SIZE
        with open(resource_path(f"levels/{Configuratuion.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in Configuratuion.MAP:
                    name = Configuratuion.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        Configuratuion.spawn_coordinates_x = ["" for i in range(Configuratuion.total_enemy)]
        Configuratuion.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        Configuratuion.spawn_coordinates_x[0] = random.choice(Configuratuion.coordinates_lst) # Создание списка координат появления
        for i in range(1, Configuratuion.total_enemy):              # Создание списка координат появления
            lst = Configuratuion.coordinates_lst.copy()
            lst.remove(Configuratuion.spawn_coordinates_x[i - 1])
            Configuratuion.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(Configuratuion.spawn_coordinates_x[0]) # Создание первой метки появления
        
    if game_over:
        show_game_over_screen()
        game_over = False
        before_start = True
        Configuratuion.graph.walls = []
    
    if level_won:
        if Configuratuion.level_number == 30:
            Configuratuion.level_number = 1
        else:
            Configuratuion.level_number += 1
        level_won = False

        Configuratuion.graph.walls = []

        Configuratuion.start_time = pygame.time.get_ticks()
        Configuratuion.enemy_respawn_time = Configuratuion.start_time
        Configuratuion.last_enemy_hit_time = Configuratuion.start_time
        Configuratuion.last_player_hit_time = Configuratuion.start_time
        Configuratuion.powerup_hit_time = Configuratuion.start_time 
        try:
            Configuratuion.game_start_sound.play()
        except:
            pass
        Configuratuion.all_sprites = pygame.sprite.Group()
        Configuratuion.enemies = pygame.sprite.Group()
        Configuratuion.new_enemies = pygame.sprite.Group()
        Configuratuion.enemies_on_ice = pygame.sprite.Group()
        Configuratuion.enemies_mode1 = pygame.sprite.Group()
        Configuratuion.enemies_mode2 = pygame.sprite.Group()
        Configuratuion.enemies_mode3 = pygame.sprite.Group()
        Configuratuion.player_bullets = pygame.sprite.Group()
        Configuratuion.enemy_bullets = pygame.sprite.Group()
        Configuratuion.powerups = pygame.sprite.Group()
        Configuratuion.tiles = pygame.sprite.Group()
        Configuratuion.spawns = pygame.sprite.Group()
        Configuratuion.shields = pygame.sprite.Group()
        Configuratuion.layers = pygame.sprite.LayeredUpdates()
        
        Configuratuion.player = Player(Configuratuion.player_image, Configuratuion.player_level, Configuratuion.player_lives)
        Configuratuion.player.level = Configuratuion.player_level
        Configuratuion.player.first_image = Configuratuion.player_image
        Configuratuion.shield = Shield(Configuratuion.player.rect.center)
        Configuratuion.base = Base()
        
        Configuratuion.current_score = ""
        Configuratuion.current_score_centerx = -100
        Configuratuion.current_score_top = -100
        Configuratuion.total_enemy = 5
        Configuratuion.remaining_enemy_count = Configuratuion.total_enemy
        Configuratuion.current_enemy_count = 0
        Configuratuion.total_enemy_count = 0
        Configuratuion.new_enemies_number = 0
        Configuratuion.hits_interval = 0
        Configuratuion.base_shield_start_time = 0
        Configuratuion.base_shield = False
        Configuratuion.freeze_time = 0
        Configuratuion.frozen_time = False
        Configuratuion.game_over_string = ""
        Configuratuion.game_over_string_centerx = -100
        Configuratuion.game_over_string_top = -100

        # Создание стен
        s = Configuratuion.TILE_SIZE
        with open(resource_path(f"levels/{Configuratuion.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in Configuratuion.MAP:
                    name = Configuratuion.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        Configuratuion.spawn_coordinates_x = ["" for i in range(Configuratuion.total_enemy)]
        Configuratuion.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        Configuratuion.spawn_coordinates_x[0] = random.choice(Configuratuion.coordinates_lst) # Создание списка координат появления
        for i in range(1, Configuratuion.total_enemy):              # Создание списка координат появления
            lst = Configuratuion.coordinates_lst.copy()
            lst.remove(Configuratuion.spawn_coordinates_x[i - 1])
            Configuratuion.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(Configuratuion.spawn_coordinates_x[0]) # Создание первой метки появления

    # Держим цикл на правильной скорости
    Configuratuion.clock.tick(Configuratuion.FPS)

    ##### Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    
    ##### Обновление
    Configuratuion.all_sprites.update()
    Configuratuion.now = pygame.time.get_ticks()
    Configuratuion.formatted_now_time = get_time() 
    
    # Добавление первых противников и меток появления
    enemies_lst = [NormalEnemy] # Список подклассов противника
    if Configuratuion.total_enemy_count < 3 and Configuratuion.now - Configuratuion.enemy_respawn_time >= Configuratuion.appearance_delay:
        Configuratuion.enemy_respawn_time = Configuratuion.now
        random.choice(enemies_lst)(Configuratuion.total_enemy_count, Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count]) # Создание противника
        Configuratuion.current_enemy_count += 1
        Configuratuion.total_enemy_count += 1
        if Configuratuion.total_enemy_count < 3:
            Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])

    # Добавление остальных противников и меток появления
    if Configuratuion.now - Configuratuion.enemy_respawn_time >= Configuratuion.appearance_delay and Configuratuion.remaining_enemy_count >= 3 and Configuratuion.current_enemy_count < 3:
        if Configuratuion.current_enemy_count == 2 and Configuratuion.new_enemies_number == 0:
            Configuratuion.enemy_respawn_time = Configuratuion.now
        if Configuratuion.current_enemy_count == 1 and Configuratuion.new_enemies_number == 0:
            Configuratuion.enemy_respawn_time += Configuratuion.hits_interval
        if Configuratuion.new_enemies_number != 0: # После применения улучшения Gun
            Configuratuion.enemy_respawn_time = Configuratuion.now
        random.choice(enemies_lst)(Configuratuion.total_enemy_count, Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])
        Configuratuion.current_enemy_count += 1
        Configuratuion.total_enemy_count += 1
        while Configuratuion.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])
            Configuratuion.new_enemies_number -= 1

    # Добавление последних противников
    if (Configuratuion.now - Configuratuion.enemy_respawn_time >= Configuratuion.appearance_delay and Configuratuion.remaining_enemy_count < 3 
        and Configuratuion.remaining_enemy_count != Configuratuion.current_enemy_count):
        Configuratuion.enemy_respawn_time = Configuratuion.now
        random.choice(enemies_lst)(Configuratuion.total_enemy_count, Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])
        Configuratuion.current_enemy_count += 1
        Configuratuion.total_enemy_count += 1
        while Configuratuion.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(Configuratuion.spawn_coordinates_x[Configuratuion.total_enemy_count])
            Configuratuion.new_enemies_number -= 1
    
    # Добавление обработки столкновений
    collisions.collide()

    # Если прошла ли 1 секунда после появления локальных очков
    if Configuratuion.now - Configuratuion.last_enemy_hit_time > 1000 and Configuratuion.now - Configuratuion.powerup_hit_time > 1000:
        Configuratuion.current_score = ""

    # Если у игрока кончились жизни, игра окончена
    if Configuratuion.player.lives == 0 and Configuratuion.now - Configuratuion.last_player_hit_time > 2000 and not before_start:
        try:
            Configuratuion.game_over_sound.play()
        except:
            pass
        game_over = True

    # Если противники закончились, уровень пройден
    if (Configuratuion.remaining_enemy_count == 0 and Configuratuion.now - Configuratuion.last_enemy_hit_time > 2000 and
        Configuratuion.now - Configuratuion.powerup_hit_time > 2000):
        Configuratuion.player_image = Configuratuion.player.first_image
        Configuratuion.player_level = Configuratuion.player.level
        Configuratuion.player_lives = Configuratuion.player.lives
        level_won = True

    # Если прошло время заморозки противников
    if Configuratuion.frozen_time:
        if Configuratuion.now - Configuratuion.freeze_time > 5000:
            for enemy in Configuratuion.enemies:
                enemy.frozen = False
            Configuratuion.frozen_time = False

    # Если база уничтожена
    if Configuratuion.base.destroyed and not before_start:
        if Configuratuion.game_over_string_top > Configuratuion.HEIGHT / 2:
            Configuratuion.game_over_string_top -= 3
        for enemy in Configuratuion.enemies_mode3:
            enemy.change_mode(3, 1)
        for enemy in Configuratuion.enemies_mode2:
            enemy.change_mode(2, 1)

    # Если база уничтожена, игра окончена
    if Configuratuion.base.destroyed and Configuratuion.now - Configuratuion.base.destroyed_time > 3000 and not before_start:
        Configuratuion.player.kill()
        Configuratuion.player_level = 0
        Configuratuion.player_image = Configuratuion.player_images[0]
        game_over = True

    # Если движение противника парализовано, сменить режим на №1
    for enemy in Configuratuion.enemies_mode2:
        if enemy.moving_blocked == True and pygame.time.get_ticks() - enemy.moving_blocked_time > enemy.timeout:
            enemy.change_mode(2, 1)
    
    for enemy in Configuratuion.enemies_mode3:
        if enemy.moving_blocked == True and pygame.time.get_ticks() - enemy.moving_blocked_time > enemy.timeout:
            enemy.change_mode(3, 1)
    
    ##### Визуализация (сборка)
    render.render()

pygame.quit()
