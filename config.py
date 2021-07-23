import pygame
import os
import math
from structures import GridWithWeights


class Config():
    WIDTH = 650 # ширина игрового окна
    WIDTH = 650 # ширина игрового окна
    HEIGHT = 650 # высота игрового окна
    FPS = 60 # частота кадров в секунду
    TILE_SIZE = 50 # размер блока карты
    TILES_IN_ROW = int(WIDTH / TILE_SIZE) # Количество ячеек в ряду
    n = TILE_SIZE / 2

    # Цвета (R, G, B)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    MAP = {
        "1": "STEEL",
        "2": "BRICK",
        "3": "GRASS",
        "4": "WATER",
        "5": "ICE",
    }


    # создаем игру и окно
    pygame.init()
    try:
        pygame.mixer.init() # для звука
        # pygame.mixer.quit()
    except Exception:
        pass
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    # настройка папки ассетов
    img_dir = os.path.join(os.path.dirname(__file__), "img")
    snd_dir = os.path.join(os.path.dirname(__file__), "snd")

    # Загрузка изображений
    player_images = []
    i = 0
    filename = ""
    img = None
    for i in range(1, 4):
        filename = f"player_01_0{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (42, 42))
        player_images.append(img)
    player_mini_img = pygame.transform.scale(player_images[0], (25, 25))

    enemy_images = []
    blue_enemy_images = []
    red_enemy_images = []
    for i in range(1, 5):
        filename = f"enemy_10{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (42, 42))
        img = pygame.transform.rotate(img, 180)
        blue_enemy_images.append(img)
    for i in range(1, 5):
        filename = f"enemy_20{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (42, 42))
        img = pygame.transform.rotate(img, 180)
        red_enemy_images.append(img)
    enemy_images.append(blue_enemy_images)
    enemy_images.append(red_enemy_images)

    base_images = []
    for i in range(1, 3):
        filename = f"base_0{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        base_images.append(img)

    bullet_img = pygame.Surface((6, 12))

    explosion_anim = []
    for i in range(1, 4):
        filename = f"expl_{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (75, 75))
        explosion_anim.append(img)

    powerup_images = {}
    powerup_images["gun"] = pygame.image.load(os.path.join(img_dir, "powerup_01.png")).convert()
    powerup_images["gun"] = pygame.transform.scale(powerup_images["gun"], (40, 40))
    powerup_images["shield"] = pygame.image.load(os.path.join(img_dir, "powerup_02.png")).convert()
    powerup_images["shield"] = pygame.transform.scale(powerup_images["shield"], (40, 40))
    powerup_images["base"] = pygame.image.load(os.path.join(img_dir, "powerup_03.png")).convert()
    powerup_images["base"] = pygame.transform.scale(powerup_images["base"], (40, 40))
    powerup_images["levelup"] = pygame.image.load(os.path.join(img_dir, "powerup_04.png")).convert()
    powerup_images["levelup"] = pygame.transform.scale(powerup_images["levelup"], (40, 40))
    powerup_images["life"] = pygame.image.load(os.path.join(img_dir, "powerup_05.png")).convert()
    powerup_images["life"] = pygame.transform.scale(powerup_images["life"], (40, 40))
    powerup_images["time"] = pygame.image.load(os.path.join(img_dir, "powerup_06.png")).convert()
    powerup_images["time"] = pygame.transform.scale(powerup_images["time"], (40, 40))

    spawn_images = []
    for i in range(1, 3):
        filename = f"spawn_0{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (42, 42))
        spawn_images.append(img)

    shield_images = []
    for i in range(1, 3):
        filename = f"shield_0{i}.png"
        img = pygame.image.load(os.path.join(img_dir, filename)).convert()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        shield_images.append(img)

    tile_images = {}
    tile_types = ["STEEL", "BRICK", "GRASS", "WATER", "WATER2", "ICE"]
    for i in range(len(tile_types)):
        img = pygame.image.load(os.path.join(img_dir, f"tile_0{i}.png")).convert()   
        img = pygame.transform.scale(img, (int(TILE_SIZE / 2), int(TILE_SIZE / 2)))
        tile_images[tile_types[i]] = img

    # Загрузка звуков
    powerup_sound = None
    try:
        game_start_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gamestart.ogg"))
        shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, "fire.ogg"))
        powerup_sound = pygame.mixer.Sound(os.path.join(snd_dir, "powerup.wav"))
        powerup_sound.set_volume(0.5)
        hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, "hit.wav"))
        explosion_sound = pygame.mixer.Sound(os.path.join(snd_dir, "explosion.ogg"))
        game_over_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gameover.ogg"))
    except:
        print("Sound_Error")


    # Цикл игры
    graph = GridWithWeights(WIDTH, HEIGHT)

    appearance_delay = 1500
    player_speed = 4
    enemy_speed = 2
    player_image = player_images[0]
    player_level = 0
    player_lives = 3
    enemy_mode1_duration = 10000
    enemy_mode2_duration = 10000

    start_time = None
    enemy_respawn_time = None
    last_enemy_hit_time = None
    last_player_hit_time = None
    powerup_hit_time = None
    all_sprites = None
    enemies = None
    new_enemies = None
    enemies_mode1 = None
    enemies_mode2 = None
    enemies_mode3 = None
    bullets = None
    player_bullets = None
    enemy_bullets = None
    powerups = None
    tiles = None
    spawns = None
    shields = None
    layers = None
    player = None
    shield = None     
    base = None
    current_score = None
    current_score_centerx = None
    current_score_top = None
    level_number = None
    total_score = None
    total_enemy = None         # Количество противников на весь уровень
    remaining_enemy_count = None # Оставшееся количество противников
    current_enemy_count = None # Текущее количество противников на карте
    total_enemy_count = None # Общее количество появившихся противников
    new_enemies_number = None # Количество противников, которое нужно добавить после применения улучшения Gun
    hits_interval = None
    base_shield_start_time = None
    base_shield = None
    freeze_time = None
    frozen_time = None
    game_over_string = None
    game_over_string_centerx = None
    game_over_string_top = None
    spawn_coordinates_x = None
    coordinates_lst = None
    now = None
