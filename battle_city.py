import pygame
import random
import os
import math
from player import Player
from mob import Enemy, NormalEnemy, FastEnemy, EnhancedEnemy, HeavyEnemy


def get_time():
    now = pygame.time.get_ticks()
    current_seconds = math.trunc((now - start_time) / 1000)
    current_minutes = 0
    while current_seconds >= 60:
        current_minutes += 1
        current_seconds -= 60
    if current_seconds < 10:
        current_seconds = f"0{str(current_seconds)}"
    if current_minutes < 10:
        minutes = f"0{str(current_minutes)}"
    current_time = f"{str(current_minutes)}:{str(current_seconds)}"
    return current_time


def draw_text(surf, x, y, text, size, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life_bar(surf, x, y, pict1, pict2):
    if pict2 < 0:
        pict2 = 0
    if pict1 < 0:
        pict1 = 0
    LIFE_BAR_LENGTH = 100 * 2 / 3
    ARMOR_BAR_LENGTH = pict2 * 2 / 3
    BAR_TOTAL_LENGTH = LIFE_BAR_LENGTH + ARMOR_BAR_LENGTH
    BAR_HEIGHT = 10
    outline_rect = pygame.Rect(x, y, BAR_TOTAL_LENGTH, BAR_HEIGHT)
    fill_rect1 = pygame.Rect(x, y, pict1 * 2 / 3, BAR_HEIGHT)
    fill_rect2 = pygame.Rect(x + LIFE_BAR_LENGTH, y, pict2 * 2 / 3, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect1)
    pygame.draw.rect(surf, WHITE, fill_rect2)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img.set_colorkey(BLACK)
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
  

def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, WIDTH / 2, HEIGHT / 4, "Battle City", 64)
    draw_text(screen, WIDTH / 2, HEIGHT / 2, "Arrow keys to move, Space to fire", 22)
    draw_text(screen, WIDTH / 2, HEIGHT * 3 / 4, "Press ENTER to begin", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False


def show_game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, WIDTH / 2, HEIGHT / 2 - 70, "GAME OVER", 70)
    draw_text(screen, WIDTH / 2, HEIGHT * 3 / 4, "Press any key to continue", 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


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


# создаем игру и окно
pygame.init()
try:
    pygame.mixer.init() # для звука
    # pygame.mixer.quit()
except Exception:
    pass
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle city")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("Arial")

# настройка папки ассетов
img_dir = os.path.join(os.path.dirname(__file__), "img")
snd_dir = os.path.join(os.path.dirname(__file__), "snd")
    

class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = base_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 600
        self.has_shield = False
        self.shield_duration = 10000
        self.shield_start_time = None
        self.destroyed = False
        self.destroyed_time = None

        all_sprites.add(self)

    def clear_wall(self):
        for tile in tiles: 
            if (5 * 50 <= tile.rect.x < 6 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                6 * 50 <= tile.rect.x < 7 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                7 * 50 <= tile.rect.x < 8 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                5 * 50 <= tile.rect.x < 6 * 50 and 12 * 50 <= tile.rect.y < 13 * 50 or
                7 * 50 <= tile.rect.x < 8 * 50 and 12 * 50 <= tile.rect.y < 13 * 50):
                tile.kill()
    
    def create_wall(self, tile_type: str):
        x_left = base.rect.x - 50

        # Создание трёх верхних блоков
        for i in range(3):  
            tile = Tile(x_left + i * 50, base.rect.y - 50, tile_type)
            tile = Tile(x_left + 25 + i * 50, base.rect.y - 50, tile_type)
            tile = Tile(x_left + i * 50, base.rect.y - 25, tile_type)
            tile = Tile(x_left + 25 + i * 50, base.rect.y - 25, tile_type)

        # Создание двух боковых блоков
        for i in range(2):
            tile = Tile(x_left + i * 100, base.rect.y, tile_type)
            tile = Tile(x_left + 25 + i * 100, base.rect.y, tile_type)
            tile = Tile(x_left + i * 100, base.rect.y + 25, tile_type)
            tile = Tile(x_left + 25 + i * 100, base.rect.y + 25, tile_type)

    def upgrade_wall(self):
        self.has_shield = True
        self.shield_start_time = pygame.time.get_ticks()
        self.clear_wall()
        self.create_wall("STEEL")
    
    def downgrade_wall(self):
        self.has_shield = False
        self.clear_wall()   
        self.create_wall("BRICK")

    def update(self):
        # Проверка, не прошло ли время действия защиты базы
        if self.has_shield:
            if now - self.shield_start_time > self.shield_duration:
                self.shield_start_time = None
                self.downgrade_wall()
        
        if self.destroyed:
            self.image = base_images[1]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 300
            self.rect.y = 600


class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, direction, speed=10, strength=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.direction = direction
        self.speedx = speed
        self.speedy = -speed
        self.strength = strength
        self.rotate(self.direction)
        
        all_sprites.add(self)
        bullets.add(self)
        layers.add(self)

    def rotate(self, direction):
        angle = 0
        if direction == "up":
            angle = 0
        elif direction == "right":
            angle = -90
        elif direction == "down":
            angle = -180
        elif direction == "left":
            angle = 90
        new_image = pygame.transform.rotate(bullet_img, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        # Проверка направления движения пули
        if self.direction == "up":
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()
        if self.direction == "right":
            self.rect.x += self.speedx
            if self.rect.left > WIDTH:
                self.kill()
        if self.direction == "down":
            self.rect.y -= self.speedy
            if self.rect.top > HEIGHT:
                self.kill()
        if self.direction == "left":
            self.rect.x -= self.speedx
            if self.rect.right < 0:
                self.kill()


class PlayerBullet(Bullet):
    pass
        

class EnemyBullet(Bullet):
    pass


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120

        all_sprites.add(self)
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["gun", "shield", "base", "levelup", "life", "time"])
        self.image = powerup_images[self.type] # ["gun", "shield", "base", "levelup", "life", "time"]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

        all_sprites.add(self)
        powerups.add(self)

    def update(self):
        pass


class Spawn(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = spawn_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

        all_sprites.add(self)
        spawns.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame)) # 0 либо 1
            centerx = self.rect.centerx
            self.image = spawn_images[self.frame]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.y = 0


class Shield(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = shield_images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.spawn_time = pygame.time.get_ticks()
        self.existance_time = 4000

        all_sprites.add(self)
        shields.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.existance_time:
            self.kill()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame))
            self.image = shield_images[self.frame]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
        self.rect.center = player.rect.center


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer = 0
        self.type = tile_type
        self.image = tile_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y     

        if self.type == "STEEL":
            self.layer = 0
        if self.type == "BRICK":
            self.layer = 0
        if self.type == "GRASS":
            self.layer = 1
        if self.type == "WATER":
            self.subtype = 0
            self.layer = -1
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 120
        if self.type == "ICE":
            self.layer = -1

        all_sprites.add(self)
        tiles.add(self)
        layers.add(self)
        
    def update(self):
        if self.type == 'WATER':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.subtype = int(not bool(self.subtype))
                if self.subtype == 1:
                    self.image = tile_images["WATER2"]
                    self.image.set_colorkey(BLACK)   
                if self.subtype == 0:
                    self.image = tile_images["WATER"]
                    self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y


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


MAP = {
    "1": "STEEL",
    "2": "BRICK",
    "3": "GRASS",
    "4": "WATER",
    "5": "ICE",
}


# Цикл игры
appearance_delay = 1500
player_speed = 4
enemy_speed = 4
player_image = player_images[0]
player_level = 0
player_lives = 3
before_start = True
level_won = False
running = True
game_over = False
while running:
    if before_start:  
        show_start_screen()
        before_start = False
        start_time = pygame.time.get_ticks()
        enemy_respawn_time = start_time
        last_enemy_hit_time = start_time
        last_player_hit_time = start_time
        powerup_hit_time = start_time
        try:
            game_start_sound.play()
        except NameError:
            pass
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        new_enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        tiles = pygame.sprite.Group()
        spawns = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        layers = pygame.sprite.LayeredUpdates()
        player = Player(player_image)
        shield = Shield(player.rect.center)     
        base = Base()
        
        current_score = ""
        current_score_centerx = -100
        current_score_top = -100
        level_number = 1
        total_score = 0
        total_enemy = 5
        remaining_enemy_count = total_enemy
        current_enemy_count = 0
        total_enemy_count = 0
        new_enemies_number = 0
        base_shield_start_time = 0
        base_shield = False
        freeze_time = 0
        frozen_time = False
        
        game_over_string = ""
        game_over_string_centerx = -100
        game_over_string_top = -100

        # Создание стен
        s = TILE_SIZE
        with open(f"levels/{level_number}.txt", "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in MAP:
                    name = MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание spawn
        spawn_centerxs = ["" for i in range(total_enemy)]
        coordinates_lst = [25, WIDTH / 2, WIDTH - 25]
        spawn_centerxs[0] = random.choice(coordinates_lst) # Создание списка координат появления
        for i in range(1, total_enemy):              # Создание списка координат появления
            lst = coordinates_lst.copy()
            lst.remove(spawn_centerxs[i - 1])
            spawn_centerxs[i] = random.choice(lst)
        spawn = Spawn(spawn_centerxs[0]) # Создание первого spawn
        
    if game_over:
        show_game_over_screen()
        game_over = False
        before_start = True
    
    if level_won:
        if level_number == 30:
            level_number = 1
        else:
            level_number += 1
        level_won = False

        start_time = pygame.time.get_ticks()
        enemy_respawn_time = start_time
        last_enemy_hit_time = start_time
        last_player_hit_time = start_time
        powerup_hit_time = start_time 
        try:
            game_start_sound.play()
        except NameError:
            pass
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        new_enemies = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        tiles = pygame.sprite.Group()
        spawns = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        layers = pygame.sprite.LayeredUpdates()
        player = Player(player_image, player_level, player_lives)
        player.level = player_level
        player.first_image = player_image
        shield = Shield(player.rect.center)
        base = Base()
        
        current_score = ""
        current_score_centerx = -100
        current_score_top = -100
        total_enemy = 5
        remaining_enemy_count = total_enemy
        current_enemy_count = 0
        total_enemy_count = 0
        new_enemies_number = 0
        base_shield_start_time = 0
        base_shield = False
        freeze_time = 0
        frozen_time = False
        game_over_string = ""
        game_over_string_centerx = -100
        game_over_string_top = -100

        # Создание стен
        s = TILE_SIZE
        with open(f"levels/{level_number}.txt", "rt") as f:
            lines = f.readlines()
        for i in range(13):
            for j in range(13):
                if lines[i][j] in MAP:
                    name = MAP[lines[i][j]]
                    Tile(j * s, i * s, name)
                    Tile(j * s + s / 2, i * s, name)
                    Tile(j * s, i * s + s / 2, name)
                    Tile(j * s + s / 2, i * s + s / 2, name)

        # Создание spawn
        spawn_centerxs = ["" for i in range(total_enemy)]
        coordinates_lst = [25, WIDTH / 2, WIDTH - 25]
        spawn_centerxs[0] = random.choice(coordinates_lst) # Создание списка координат появления
        for i in range(1, total_enemy):              # Создание списка координат появления
            lst = coordinates_lst.copy()
            lst.remove(spawn_centerxs[i - 1])
            spawn_centerxs[i] = random.choice(lst)
        spawn = Spawn(spawn_centerxs[0]) # Создание первого spawn

    # Держим цикл на правильной скорости
    clock.tick(FPS)

    ##### Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    
    ##### Обновление
    all_sprites.update()
    now = pygame.time.get_ticks()
    formatted_now_time = get_time() 

    # Проверка, прошла ли 1 секунда после появления локальных очков
    if now - last_enemy_hit_time > 1000 and now - powerup_hit_time > 1000:
        current_score = ""

    # Добавление первых противников и spawns
    enemies_lst = [NormalEnemy, FastEnemy, EnhancedEnemy, HeavyEnemy] # Список подклассов противника
    if total_enemy_count < 3 and now - enemy_respawn_time >= appearance_delay:
        enemy_respawn_time = now
        enemy = random.choice(enemies_lst)(spawn_centerxs[total_enemy_count])
        current_enemy_count += 1
        total_enemy_count += 1
        if total_enemy_count < 3:
            spawn = Spawn(spawn_centerxs[total_enemy_count])

    # Добавление остальных противников и spawns
    if now - enemy_respawn_time >= appearance_delay and remaining_enemy_count >= 3 and current_enemy_count < 3:
        if current_enemy_count == 2 and new_enemies_number == 0:
            enemy_respawn_time = now
        if current_enemy_count == 1 and new_enemies_number == 0:
            enemy_respawn_time += hits_interval
        if new_enemies_number != 0: # После применения улучшения Gun
            enemy_respawn_time = now
        enemy = random.choice(enemies_lst)(spawn_centerxs[total_enemy_count])
        current_enemy_count += 1
        total_enemy_count += 1
        while new_enemies_number != 0: # После применения улучшения Gun
            spawn = Spawn(spawn_centerxs[total_enemy_count])
            new_enemies_number -= 1

    # Добавление последних противников
    if (now - enemy_respawn_time >= appearance_delay and remaining_enemy_count < 3 
        and remaining_enemy_count != current_enemy_count):
        enemy_respawn_time = now
        enemy = random.choice(enemies_lst)(spawn_centerxs[total_enemy_count])
        current_enemy_count += 1
        total_enemy_count += 1
        while new_enemies_number != 0: # После применения улучшения Gun
            spawn = Spawn(spawn_centerxs[total_enemy_count])
            new_enemies_number -= 1
    
    # Проверка столкновений противников и spawns
    hits = pygame.sprite.groupcollide(new_enemies, spawns, False, True)
    for hit in hits:
        hit.remove(new_enemies)
        hit.add(enemies)
    
    # Проверка столкновений пули противника и пули игрока
    hits = pygame.sprite.groupcollide(player_bullets, enemy_bullets, True, True)

    # Проверка столкновений пули игрока с элементом стены
    hits = pygame.sprite.groupcollide(tiles, player_bullets, False, False)
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
    hits = pygame.sprite.groupcollide(tiles, enemy_bullets, False, False)
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

    # Проверка, не ударила ли пуля щит
    for shield in shields:
        hits = pygame.sprite.spritecollide(shield, enemy_bullets, True)

    # Проверка столкновений пули противника и игрока
    if not shield.alive():
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            last_player_hit_time = now
            if player.armor > 100:
                player.armor -= 100
            elif player.armor > 0:
                player.life -= 100 - player.armor
                player.armor = 0
            elif player.armor == 0:
                player.life -= 100

            if player.life > 0:
                try:
                    hit_sound.play()
                except NameError:
                    pass
            else:
                explosion = Explosion(hit.rect.center)
                player.hide()
                player.lives -= 1
                player.downgrade(player.rect.center)
                try:
                    explosion_sound.play()
                except NameError:
                    pass
    # Если игрок умер, игра окончена
    if player.lives == 0 and now - last_player_hit_time > 2000 and not before_start:
        try:
            game_over_sound.play()
        except NameError:
            pass
        game_over = True
    
    # Проверка столкновений пули игрока и противника
    hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
    for hit in hits:
        hits_interval = now - last_enemy_hit_time
        last_enemy_hit_time = now

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
                hit_sound.play()
            except NameError:
                pass
        else:                       # Если противник убит
            current_score = 100
            current_score_centerx = hit.rect.centerx + 20
            current_score_top = hit.rect.top + 20
            current_enemy_count -= 1
            remaining_enemy_count -= 1
            if current_enemy_count == 2:
                enemy_respawn_time = now
            if remaining_enemy_count >= 3:
                if current_enemy_count == 2:
                    spawn = Spawn(spawn_centerxs[total_enemy_count]) 
                if current_enemy_count == 1:
                    spawn = Spawn(spawn_centerxs[total_enemy_count + 1]) 
            total_score += 100
            explosion = Explosion(hit.rect.center)
            hit.kill()  
            try:
                explosion_sound.play()
            except NameError:
                pass
            
            if random.random() > 0.8:
                powerup = Powerup(hit.rect.center)     
    # Если противники закончились, уровень пройден
    if remaining_enemy_count == 0 and now - last_enemy_hit_time > 2000 and now - powerup_hit_time > 2000:
        player_image = player.first_image
        player_level = player.level
        player_lives = player.lives
        level_won = True
    
    # Проверка столкновений игрока с элементом стены
    hits = pygame.sprite.spritecollide(player, tiles, False)
    for hit in hits:
        if hit.type == "STEEL":
            player.stop()
            break
        if hit.type == "BRICK":
            player.stop()
            break
        if hit.type == "GRASS":
            pass
        if hit.type == "WATER":
            player.stop()
            break
        if hit.type == "ICE":
            pass

    # Проверка столкновений противника с элементом стены
    hits = pygame.sprite.groupcollide(enemies, tiles, False, False)
    for hit in hits:
        for tile in hits[hit]:
            if tile.type == "STEEL":
                hit.stop()
                hit.last_rotate = now
                hit.rotate()
                break
            if tile.type == "BRICK":
                hit.stop()
                hit.last_rotate = now
                hit.rotate()
                break
            if tile.type == "GRASS":
                pass
            if tile.type == "WATER":
                hit.stop()
                hit.last_rotate = now
                hit.rotate()
                break
            if tile.type == "ICE":
                pass
        
    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        powerup_hit_time = now
        current_score = 100
        current_score_centerx = hit.rect.centerx
        current_score_top = hit.rect.top
        total_score += 100
        try:
            powerup_sound.play()
        except NameError:
            pass
        if hit.type == "gun":
            if enemies:
                new_enemies_number = remaining_enemy_count - current_enemy_count # Количество противников,
                for enemy in enemies:                              # которое нужно добавить после очистки карты
                    enemy.kill()
                    remaining_enemy_count -= 1
                current_enemy_count = 0
                enemy_respawn_time = now
                if new_enemies_number != 0:
                    spawn = Spawn(spawn_centerxs[total_enemy_count])
                    new_enemies_number -= 1
        if hit.type == "shield":
            if shield.alive():
                shield.kill()
            shield = Shield(player.rect.center)
        if hit.type == "base":
            base.upgrade_wall()
        if hit.type == "levelup":
            player.upgrade(player.rect.center, player.direction)
        if hit.type == "life":
            player.lives += 1
            if player.lives >= 5:
                player.lives = 5
                player.life = 100
        if hit.type == "time":
            frozen_time = True
            freeze_time = now
            for enemy in enemies:
                enemy.frozen = True 
    
    # Проверка, не прошло ли время заморозки противников
    if frozen_time:
        if now - freeze_time > 5000:
            for enemy in enemies:
                enemy.frozen = False
            frozen_time = False

    # Проверка столкновений противника и игрока
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in hits:
        player.stop()
        hit.stop()
        hit.last_rotate = now
        hit.reverse()
 
    # Проверка столкновений противников друг с другом
    for enemy in enemies:
        enemy.remove(enemies)        
        hits = pygame.sprite.spritecollide(enemy, enemies, False)
        for hit in hits:
            if hit.frozen != True:
                hit.stop()
                hit.last_rotate = now
                hit.reverse()
            if enemy.frozen != True:
                enemy.stop() 
                enemy.last_rotate = now
                enemy.reverse()            
            
        enemy.add(enemies)

    # Проверка столкновений игрока и базы
    if pygame.sprite.collide_rect(player, base):
        player.stop()
    
    # Проверка столкновений противников и базы
    hits = pygame.sprite.spritecollide(base, enemies, False)
    for hit in hits:
        hit.stop()
        hit.last_rotate = now
        hit.rotate()
    
    # Проверка столкновений пули игрока и базы
    hits1 = pygame.sprite.spritecollide(base, player_bullets, True)
    
    # Проверка столкновений пули противников и базы
    hits2 = pygame.sprite.spritecollide(base, enemy_bullets, True)
    if hits1 or hits2:
        if not base.destroyed:
            explosion = Explosion(base.rect.center)
            base.destroyed = True
            base.destroyed_time = now
            try:
                game_over_sound.play()
            except NameError:
                pass
            game_over_string = "GAME OVER"
            game_over_string_centerx = base.rect.centerx
            game_over_string_top = base.rect.top
    
    # Если база уничтожена, показать строку "GAME OVER"
    if base.destroyed and not before_start:
        if game_over_string_top > HEIGHT / 2:
            game_over_string_top -= 3
    
    # Если база уничтожена, игра окончена
    if base.destroyed and now - base.destroyed_time > 3000 and not before_start:
        player.kill()
        player_level = 0
        player_image = player_images[0]
        game_over = True
    
    ##### Визуализация (сборка)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    layers.draw(screen)
    draw_text(screen, WIDTH / 3, 5, str(formatted_now_time), 24)                        # Время
    draw_text(screen, WIDTH / 3 * 2 - 25, 5, str(total_score), 24)                      # Очки
    draw_life_bar(screen, 5, 10, player.life, player.armor)                             # Уровень жизни
    draw_lives(screen, WIDTH - 30, 5, player.lives, player_mini_img)                    # Количество жизней
    draw_text(screen, current_score_centerx, current_score_top, str(current_score), 18) # Локальные очки
    draw_text(screen, game_over_string_centerx, game_over_string_top, game_over_string, 45)   # "GAME OVER"

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
