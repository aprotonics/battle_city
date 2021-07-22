import pygame
import random
import os
import sys
import math
import datetime
from config import Config
from structures import PriorityQueue, GridWithWeights
from characters.player import Player
from characters.mob import Enemy, NormalEnemy, FastEnemy, EnhancedEnemy, HeavyEnemy
from classes import Shield, Base, Tile, Spawn
import collisions
import render


def create_path(start, goal):
    start_time = datetime.datetime.now()

    came_from, cost_so_far, iterations = a_star_search(Config.graph, start, goal)

    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()

    end_time = datetime.datetime.now()
    print("time", end_time - start_time)
    print("iterations", iterations)

    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    iterations = 0
    frontier = PriorityQueue() # Граница
    frontier.push(start, 0)
    came_from = {} # Откуда пришли
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    # Обход графа
    while not frontier.empty():
        current = frontier.extract()

        if current == goal:
            break

        for element in graph.neighbours(current):
            iterations += 1
            new_cost = cost_so_far[current] + graph.cost(current, element)
            if element not in cost_so_far or new_cost < cost_so_far[element]:
                cost_so_far[element] = new_cost
                priority = new_cost + heuristic(goal, element)
                frontier.push(element, priority)
                came_from[element] = current
    
    return came_from, cost_so_far, iterations


def get_time():
    now = pygame.time.get_ticks()
    current_seconds = math.trunc((now - Config.start_time) / 1000)
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
    font = pygame.font.Font(Config.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_start_screen():
    Config.screen.fill(Config.BLACK)
    draw_text(Config.screen, Config.WIDTH / 2, Config.HEIGHT / 4, "Battle City", 64)
    draw_text(Config.screen, Config.WIDTH / 2, Config.HEIGHT / 2, "Arrow keys to move, Space to fire", 22)
    draw_text(Config.screen, Config.WIDTH / 2, Config.HEIGHT * 3 / 4, "Press ENTER to begin", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        Config.clock.tick(Config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False


def show_game_over_screen():
    Config.screen.fill(Config.BLACK)
    draw_text(Config.screen, Config.WIDTH / 2, Config.HEIGHT / 2 - 70, "GAME OVER", 70)
    draw_text(Config.screen, Config.WIDTH / 2, Config.HEIGHT * 3 / 4, "Press any key to continue", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        Config.clock.tick(Config.FPS)
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
Config.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption("Battle city")
Config.clock = pygame.time.Clock()
Config.font_name = pygame.font.match_font("Arial")




Config.graph = GridWithWeights(Config.WIDTH, Config.HEIGHT)

## Алгоритм поиска пути
Config.start = (0 * 50, 0 * 50)
Config.goal = (4 * 50, 12 * 50)

# Создание пути
Config.path = create_path(Config.start, Config.goal)

print(Config.path)
print()


# Цикл игры
before_start = True
level_won = False
running = True
game_over = False
while running:
    if before_start: 
        show_start_screen()
        before_start = False
        Config.start_time = pygame.time.get_ticks()
        Config.enemy_respawn_time = Config.start_time
        Config.last_enemy_hit_time = Config.start_time
        Config.last_player_hit_time = Config.start_time
        Config.powerup_hit_time = Config.start_time
        try:
            Config.game_start_sound.play()
        except:
            pass
        Config.all_sprites = pygame.sprite.Group()
        Config.enemies = pygame.sprite.Group()
        Config.new_enemies = pygame.sprite.Group()
        Config.enemies_mode1 = pygame.sprite.Group()
        Config.enemies_mode2 = pygame.sprite.Group()
        Config.bullets = pygame.sprite.Group()
        Config.player_bullets = pygame.sprite.Group()
        Config.enemy_bullets = pygame.sprite.Group()
        Config.powerups = pygame.sprite.Group()
        Config.tiles = pygame.sprite.Group()
        Config.spawns = pygame.sprite.Group()
        Config.shields = pygame.sprite.Group()
        Config.layers = pygame.sprite.LayeredUpdates()
        
        Config.player = Player(Config.player_image)
        Config.shield = Shield(Config.player.rect.center)     
        Config.base = Base()
        
        Config.current_score = ""
        Config.current_score_centerx = -100
        Config.current_score_top = -100
        Config.level_number = 1
        Config.total_score = 0
        Config.total_enemy = 5         # Количество противников на весь уровень
        Config.remaining_enemy_count = Config.total_enemy # Оставшееся количество противников
        Config.current_enemy_count = 0 # Текущее количество противников на карте
        Config.total_enemy_count = 0 # Общее количество появившихся противников
        Config.new_enemies_number = 0 # Количество противников, которое нужно добавить после применения улучшения Gun
        Config.hits_interval = 0
        Config.base_shield_start_time = 0
        Config.base_shield = False
        Config.freeze_time = 0
        Config.frozen_time = False
        
        Config.game_over_string = ""
        Config.game_over_string_centerx = -100
        Config.game_over_string_top = -100

        # Создание стен
        s = Config.TILE_SIZE
        with open(resource_path(f"levels/{Config.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in Config.MAP:
                    name = Config.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        Config.spawn_coordinates_x = ["" for i in range(Config.total_enemy)]
        Config.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        Config.spawn_coordinates_x[0] = random.choice(Config.coordinates_lst) # Создание списка координат появления
        for i in range(1, Config.total_enemy):              # Создание списка координат появления
            lst = Config.coordinates_lst.copy()
            lst.remove(Config.spawn_coordinates_x[i - 1])
            Config.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(Config.spawn_coordinates_x[0]) # Создание первой метки появления
        
    if game_over:
        show_game_over_screen()
        game_over = False
        before_start = True
    
    if level_won:
        if Config.level_number == 30:
            Config.level_number = 1
        else:
            Config.level_number += 1
        level_won = False

        Config.start_time = pygame.time.get_ticks()
        Config.enemy_respawn_time = Config.start_time
        Config.last_enemy_hit_time = Config.start_time
        Config.last_player_hit_time = Config.start_time
        Config.powerup_hit_time = Config.start_time 
        try:
            Config.game_start_sound.play()
        except:
            pass
        Config.all_sprites = pygame.sprite.Group()
        Config.enemies = pygame.sprite.Group()
        Config.new_enemies = pygame.sprite.Group()
        Config.player_bullets = pygame.sprite.Group()
        Config.enemy_bullets = pygame.sprite.Group()
        Config.powerups = pygame.sprite.Group()
        Config.tiles = pygame.sprite.Group()
        Config.spawns = pygame.sprite.Group()
        Config.shields = pygame.sprite.Group()
        Config.layers = pygame.sprite.LayeredUpdates()
        
        Config.player = Player(Config.player_image, Config.player_level, Config.player_lives)
        Config.player.level = Config.player_level
        Config.player.first_image = Config.player_image
        Config.shield = Shield(Config.player.rect.center)
        Config.base = Base()
        
        Config.current_score = ""
        Config.current_score_centerx = -100
        Config.current_score_top = -100
        Config.total_enemy = 5
        Config.remaining_enemy_count = Config.total_enemy
        Config.current_enemy_count = 0
        Config.total_enemy_count = 0
        Config.new_enemies_number = 0
        Config.hits_interval = 0
        Config.base_shield_start_time = 0
        Config.base_shield = False
        Config.freeze_time = 0
        Config.frozen_time = False
        Config.game_over_string = ""
        Config.game_over_string_centerx = -100
        Config.game_over_string_top = -100

        # Создание стен
        s = Config.TILE_SIZE
        with open(resource_path(f"levels/{Config.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in Config.MAP:
                    name = Config.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        Config.spawn_coordinates_x = ["" for i in range(Config.total_enemy)]
        Config.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        Config.spawn_coordinates_x[0] = random.choice(Config.coordinates_lst) # Создание списка координат появления
        for i in range(1, Config.total_enemy):              # Создание списка координат появления
            lst = Config.coordinates_lst.copy()
            lst.remove(Config.spawn_coordinates_x[i - 1])
            Config.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(Config.spawn_coordinates_x[0]) # Создание первой метки появления

    # Держим цикл на правильной скорости
    Config.clock.tick(Config.FPS)

    ##### Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    
    ##### Обновление
    Config.all_sprites.update()
    Config.now = pygame.time.get_ticks()
    Config.formatted_now_time = get_time() 
    
    # Добавление первых противников и меток появления
    enemies_lst = [NormalEnemy] # Список подклассов противника
    if Config.total_enemy_count < 3 and Config.now - Config.enemy_respawn_time >= Config.appearance_delay:
        Config.enemy_respawn_time = Config.now
        random.choice(enemies_lst)(Config.total_enemy_count, Config.spawn_coordinates_x[Config.total_enemy_count]) # Создание противника
        Config.current_enemy_count += 1
        Config.total_enemy_count += 1
        if Config.total_enemy_count < 3:
            Spawn(Config.spawn_coordinates_x[Config.total_enemy_count])

    # Добавление остальных противников и меток появления
    if Config.now - Config.enemy_respawn_time >= Config.appearance_delay and Config.remaining_enemy_count >= 3 and Config.current_enemy_count < 3:
        if Config.current_enemy_count == 2 and Config.new_enemies_number == 0:
            Config.enemy_respawn_time = Config.now
        if Config.current_enemy_count == 1 and Config.new_enemies_number == 0:
            Config.enemy_respawn_time += Config.hits_interval
        if Config.new_enemies_number != 0: # После применения улучшения Gun
            Config.enemy_respawn_time = Config.now
        random.choice(enemies_lst)(Config.total_enemy_count, Config.spawn_coordinates_x[Config.total_enemy_count])
        Config.current_enemy_count += 1
        Config.total_enemy_count += 1
        while Config.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(Config.spawn_coordinates_x[Config.total_enemy_count])
            Config.new_enemies_number -= 1

    # Добавление последних противников
    if (Config.now - Config.enemy_respawn_time >= Config.appearance_delay and Config.remaining_enemy_count < 3 
        and Config.remaining_enemy_count != Config.current_enemy_count):
        Config.enemy_respawn_time = Config.now
        random.choice(enemies_lst)(Config.total_enemy_count, Config.spawn_coordinates_x[Config.total_enemy_count])
        Config.current_enemy_count += 1
        Config.total_enemy_count += 1
        while Config.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(Config.spawn_coordinates_x[Config.total_enemy_count])
            Config.new_enemies_number -= 1
    
    # Добавление обработки столкновений
    collisions.collide()

    # Если прошла ли 1 секунда после появления локальных очков
    if Config.now - Config.last_enemy_hit_time > 1000 and Config.now - Config.powerup_hit_time > 1000:
        Config.current_score = ""

    # Если игрок умер, игра окончена
    if Config.player.lives == 0 and Config.now - Config.last_player_hit_time > 2000 and not before_start:
        try:
            Config.game_over_sound.play()
        except:
            pass
        game_over = True

    # Если противники закончились, уровень пройден
    if (Config.remaining_enemy_count == 0 and Config.now - Config.last_enemy_hit_time > 2000 and
        Config.now - Config.powerup_hit_time > 2000):
        Config.player_image = Config.player.first_image
        Config.player_level = Config.player.level
        Config.player_lives = Config.player.lives
        level_won = True

    # Если прошло время заморозки противников
    if Config.frozen_time:
        if Config.now - Config.freeze_time > 5000:
            for enemy in Config.enemies:
                enemy.frozen = False
            Config.frozen_time = False
        
    # Если движение противника парализовано, сменить режим на №1
    for enemy in Config.enemies_mode2:
        if enemy.moving_blocked == True and pygame.time.get_ticks() - enemy.moving_blocked_time > enemy.timeout:
            enemy.change_mode(2, 1)

    # Если база уничтожена, показать строку "GAME OVER"
    if Config.base.destroyed and not before_start:
        if Config.game_over_string_top > Config.HEIGHT / 2:
            Config.game_over_string_top -= 3

    # Если база уничтожена, игра окончена
    if Config.base.destroyed and Config.now - Config.base.destroyed_time > 3000 and not before_start:
        Config.player.kill()
        Config.player_level = 0
        Config.player_image = Config.player_images[0]
        game_over = True
    
    ##### Визуализация (сборка)
    render.render()

pygame.quit()
