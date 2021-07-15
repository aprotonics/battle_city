import pygame
import os
import math


WIDTH = 650 # ширина игрового окна
HEIGHT = 650 # высота игрового окна
FPS = 60 # частота кадров в секунду
TILE_SIZE = 50 # размер блока карты

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
try:
    game_start_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gamestart.ogg"))
    shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, "fire.ogg"))
    powerup_sound = pygame.mixer.Sound(os.path.join(snd_dir, "powerup.wav"))
    powerup_sound.set_volume(0.5)
    hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, "hit.wav"))
    explosion_sound = pygame.mixer.Sound(os.path.join(snd_dir, "explosion.ogg"))
    game_over_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gameover.ogg"))
except RuntimeError:
    print("Sound_Error")





# start_time = pygame.time.get_ticks()
# enemy_respawn_time = start_time
# last_enemy_hit_time = start_time
# last_player_hit_time = start_time
# powerup_hit_time = start_time
# try:
#     game_start_sound.play()
# except NameError:
#     pass
# all_sprites = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# new_enemies = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
# player_bullets = pygame.sprite.Group()
# enemy_bullets = pygame.sprite.Group()
# powerups = pygame.sprite.Group()
# tiles = pygame.sprite.Group()
# spawns = pygame.sprite.Group()
# shields = pygame.sprite.Group()
# layers = pygame.sprite.LayeredUpdates()


# # player = Player(player_image)
# # shield = Shield(player.rect.center)     
# # base = Base()


# current_score = ""
# current_score_centerx = -100
# current_score_top = -100
# level_number = 1
# total_score = 0
# total_enemy = 5         # Количество противников на весь уровень
# remaining_enemy_count = total_enemy # Оставшееся количество противников
# current_enemy_count = 0 # Текущее количество противников на карте
# total_enemy_count = 0 # Общее количество появившихся противников
# new_enemies_number = 0 # Количество противников, которое нужно добавить после применения улучшения Gun
# hits_interval = 0
# base_shield_start_time = 0
# base_shield = False
# freeze_time = 0
# frozen_time = False

# game_over_string = ""
# game_over_string_centerx = -100
# game_over_string_top = -100



