import pygame
import random
import os
import sys
import math
import datetime
import config
from structures import PriorityQueue, GridWithWeights
from characters.player import Player
from characters.mob import Enemy, NormalEnemy, FastEnemy, EnhancedEnemy, HeavyEnemy
from classes import Shield, Base, Tile, Spawn
import collisions
import render


def create_path(start, goal):
    start_time = datetime.datetime.now()

    came_from, cost_so_far, iterations = a_star_search(config.graph, start, goal)

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
    current_seconds = math.trunc((now - config.start_time) / 1000)
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
    font = pygame.font.Font(config.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_start_screen():
    config.screen.fill(config.BLACK)
    draw_text(config.screen, config.WIDTH / 2, config.HEIGHT / 4, "Battle City", 64)
    draw_text(config.screen, config.WIDTH / 2, config.HEIGHT / 2, "Arrow keys to move, Space to fire", 22)
    draw_text(config.screen, config.WIDTH / 2, config.HEIGHT * 3 / 4, "Press ENTER to begin", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        config.clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False


def show_game_over_screen():
    config.screen.fill(config.BLACK)
    draw_text(config.screen, config.WIDTH / 2, config.HEIGHT / 2 - 70, "GAME OVER", 70)
    draw_text(config.screen, config.WIDTH / 2, config.HEIGHT * 3 / 4, "Press any key to continue", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        config.clock.tick(config.FPS)
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
config.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Battle city")
config.clock = pygame.time.Clock()
config.font_name = pygame.font.match_font("Arial")




config.graph = GridWithWeights(config.WIDTH, config.HEIGHT)

## Алгоритм поиска пути
config.start = (0 * 50, 0 * 50)
config.goal = (4 * 50, 12 * 50)

# Создание пути
config.path = create_path(config.start, config.goal)

print(config.path)
print()



# Цикл игры
config.appearance_delay = 1500
config.player_speed = 4
config.enemy_speed = 2
config.player_image = config.player_images[0]
config.player_level = 0
config.player_lives = 3
before_start = True
level_won = False
running = True
game_over = False
while running:
    if before_start: 
        show_start_screen()
        before_start = False
        config.start_time = pygame.time.get_ticks()
        config.enemy_respawn_time = config.start_time
        config.last_enemy_hit_time = config.start_time
        config.last_player_hit_time = config.start_time
        config.powerup_hit_time = config.start_time
        try:
            config.game_start_sound.play()
        except NameError:
            pass
        config.all_sprites = pygame.sprite.Group()
        config.enemies = pygame.sprite.Group()
        config.new_enemies = pygame.sprite.Group()
        config.bullets = pygame.sprite.Group()
        config.player_bullets = pygame.sprite.Group()
        config.enemy_bullets = pygame.sprite.Group()
        config.powerups = pygame.sprite.Group()
        config.tiles = pygame.sprite.Group()
        config.spawns = pygame.sprite.Group()
        config.shields = pygame.sprite.Group()
        config.layers = pygame.sprite.LayeredUpdates()
        
        config.player = Player(config.player_image)
        config.shield = Shield(config.player.rect.center)     
        config.base = Base()
        
        config.current_score = ""
        config.current_score_centerx = -100
        config.current_score_top = -100
        config.level_number = 2
        config.total_score = 0
        config.total_enemy = 5         # Количество противников на весь уровень
        config.remaining_enemy_count = config.total_enemy # Оставшееся количество противников
        config.current_enemy_count = 0 # Текущее количество противников на карте
        config.total_enemy_count = 0 # Общее количество появившихся противников
        config.new_enemies_number = 0 # Количество противников, которое нужно добавить после применения улучшения Gun
        config.hits_interval = 0
        config.base_shield_start_time = 0
        config.base_shield = False
        config.freeze_time = 0
        config.frozen_time = False
        
        config.game_over_string = ""
        config.game_over_string_centerx = -100
        config.game_over_string_top = -100

        # Создание стен
        s = config.TILE_SIZE
        with open(resource_path(f"levels/{config.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in config.MAP:
                    name = config.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        config.spawn_coordinates_x = ["" for i in range(config.total_enemy)]
        config.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        config.spawn_coordinates_x[0] = random.choice(config.coordinates_lst) # Создание списка координат появления
        for i in range(1, config.total_enemy):              # Создание списка координат появления
            lst = config.coordinates_lst.copy()
            lst.remove(config.spawn_coordinates_x[i - 1])
            config.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(config.spawn_coordinates_x[0]) # Создание первой метки появления
        
    if game_over:
        show_game_over_screen()
        game_over = False
        before_start = True
    
    if level_won:
        if config.level_number == 30:
            config.level_number = 1
        else:
            config.level_number += 1
        level_won = False

        config.start_time = pygame.time.get_ticks()
        config.enemy_respawn_time = config.start_time
        config.last_enemy_hit_time = config.start_time
        config.last_player_hit_time = config.start_time
        config.powerup_hit_time = config.start_time 
        try:
            config.game_start_sound.play()
        except NameError:
            pass
        config.all_sprites = pygame.sprite.Group()
        config.enemies = pygame.sprite.Group()
        config.new_enemies = pygame.sprite.Group()
        config.player_bullets = pygame.sprite.Group()
        config.enemy_bullets = pygame.sprite.Group()
        config.powerups = pygame.sprite.Group()
        config.tiles = pygame.sprite.Group()
        config.spawns = pygame.sprite.Group()
        config.shields = pygame.sprite.Group()
        config.layers = pygame.sprite.LayeredUpdates()
        
        config.player = Player(config.player_image, config.player_level, config.player_lives)
        config.player.level = config.player_level
        config.player.first_image = config.player_image
        config.shield = Shield(config.player.rect.center)
        config.base = Base()
        
        config.current_score = ""
        config.current_score_centerx = -100
        config.current_score_top = -100
        config.total_enemy = 5
        config.remaining_enemy_count = config.total_enemy
        config.current_enemy_count = 0
        config.total_enemy_count = 0
        config.new_enemies_number = 0
        config.hits_interval = 0
        config.base_shield_start_time = 0
        config.base_shield = False
        config.freeze_time = 0
        config.frozen_time = False
        config.game_over_string = ""
        config.game_over_string_centerx = -100
        config.game_over_string_top = -100

        # Создание стен
        s = config.TILE_SIZE
        with open(resource_path(f"levels/{config.level_number}.txt"), "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in config.MAP:
                    name = config.MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание меток появления
        config.spawn_coordinates_x = ["" for i in range(config.total_enemy)]
        config.coordinates_lst = [0 * 50, 6 * 50, 12 * 50]
        config.spawn_coordinates_x[0] = random.choice(config.coordinates_lst) # Создание списка координат появления
        for i in range(1, config.total_enemy):              # Создание списка координат появления
            lst = config.coordinates_lst.copy()
            lst.remove(config.spawn_coordinates_x[i - 1])
            config.spawn_coordinates_x[i] = random.choice(lst)
        Spawn(config.spawn_coordinates_x[0]) # Создание первой метки появления

    # Держим цикл на правильной скорости
    config.clock.tick(config.FPS)

    ##### Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    
    ##### Обновление
    config.all_sprites.update()
    config.now = pygame.time.get_ticks()
    config.formatted_now_time = get_time() 
    
    # Добавление первых противников и меток появления
    enemies_lst = [NormalEnemy] # Список подклассов противника
    if config.total_enemy_count < 3 and config.now - config.enemy_respawn_time >= config.appearance_delay:
        config.enemy_respawn_time = config.now
        random.choice(enemies_lst)(config.spawn_coordinates_x[config.total_enemy_count]) # Создание противника
        config.current_enemy_count += 1
        config.total_enemy_count += 1
        if config.total_enemy_count < 3:
            Spawn(config.spawn_coordinates_x[config.total_enemy_count])

    # Добавление остальных противников и меток появления
    if config.now - config.enemy_respawn_time >= config.appearance_delay and config.remaining_enemy_count >= 3 and config.current_enemy_count < 3:
        if config.current_enemy_count == 2 and config.new_enemies_number == 0:
            config.enemy_respawn_time = config.now
        if config.current_enemy_count == 1 and config.new_enemies_number == 0:
            config.enemy_respawn_time += config.hits_interval
        if config.new_enemies_number != 0: # После применения улучшения Gun
            config.enemy_respawn_time = config.now
        random.choice(enemies_lst)(config.spawn_coordinates_x[config.total_enemy_count])
        config.current_enemy_count += 1
        config.total_enemy_count += 1
        while config.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(config.spawn_coordinates_x[config.total_enemy_count])
            config.new_enemies_number -= 1

    # Добавление последних противников
    if (config.now - config.enemy_respawn_time >= config.appearance_delay and config.remaining_enemy_count < 3 
        and config.remaining_enemy_count != config.current_enemy_count):
        config.enemy_respawn_time = config.now
        random.choice(enemies_lst)(config.spawn_coordinates_x[config.total_enemy_count])
        config.current_enemy_count += 1
        config.total_enemy_count += 1
        while config.new_enemies_number != 0: # После применения улучшения Gun
            Spawn(config.spawn_coordinates_x[config.total_enemy_count])
            config.new_enemies_number -= 1
    
    # Добавление обработки столкновений
    collisions.collide()

    # Если прошла ли 1 секунда после появления локальных очков
    if config.now - config.last_enemy_hit_time > 1000 and config.now - config.powerup_hit_time > 1000:
        config.current_score = ""

    # Если игрок умер, игра окончена
    if config.player.lives == 0 and config.now - config.last_player_hit_time > 2000 and not before_start:
        try:
            config.game_over_sound.play()
        except NameError:
            pass
        game_over = True

    # Если противники закончились, уровень пройден
    if (config.remaining_enemy_count == 0 and config.now - config.last_enemy_hit_time > 2000 and
        config.now - config.powerup_hit_time > 2000):
        config.player_image = config.player.first_image
        config.player_level = config.player.level
        config.player_lives = config.player.lives
        level_won = True

    # Если прошло время заморозки противников
    if config.frozen_time:
        if config.now - config.freeze_time > 5000:
            for enemy in config.enemies:
                enemy.frozen = False
            config.frozen_time = False

    # Если база уничтожена, показать строку "GAME OVER"
    if config.base.destroyed and not before_start:
        if config.game_over_string_top > config.HEIGHT / 2:
            config.game_over_string_top -= 3

    # Если база уничтожена, игра окончена
    if config.base.destroyed and config.now - config.base.destroyed_time > 3000 and not before_start:
        config.player.kill()
        config.player_level = 0
        config.player_image = config.player_images[0]
        game_over = True
    
    ##### Визуализация (сборка)
    render.render()

pygame.quit()
