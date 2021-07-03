# Добавлены звуки и таймер
import pygame
import random
import os
import math


def show_go_screen():
    pass

def get_time():
    now_time = pygame.time.get_ticks()
    seconds = math.trunc((now_time - start_time) / 1000)
    minutes = 0
    while seconds >= 60:
        minutes += 1
        seconds -= 60
    if seconds < 10:
        seconds = "0" + str(seconds)
    if minutes < 10:
        minutes = "0" + str(minutes)
    time = str(minutes) + ":" + str(seconds)
    return time

def draw_text(surf, x, y, text, size):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img.set_colorkey(BLACK)
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


WIDTH = 600 # ширина игрового окна
HEIGHT = 600 # высота игрового окна
FPS = 60 # частота кадров в секунду

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# создаем игру и окно
pygame.init()
pygame.mixer.init() # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle city")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

# настройка папки ассетов
img_dir = os.path.join(os.path.dirname(__file__), "img")
snd_dir = os.path.join(os.path.dirname(__file__), "snd")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.direction = "up"
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
    
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
        new_image = pygame.transform.rotate(player_img, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        # Проверка, какая клавиша нажата. Приоритет UP -> RIGHT -> DOWN -> LEFT
        if keystate[pygame.K_UP] == True:
            self.direction = "up"
            self.rotate(self.direction)
            self.speedy = -2  
        elif keystate[pygame.K_RIGHT] == True:
            self.direction = "right"
            self.rotate(self.direction)  
            self.speedx = 2
        elif keystate[pygame.K_DOWN] == True:
            self.direction = "down"
            self.rotate(self.direction) 
            self.speedy = 2  
        elif keystate[pygame.K_LEFT] == True:
            self.direction = "left"
            self.rotate(self.direction) 
            self.speedx = -2  
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if keystate[pygame.K_SPACE] == True:
            self.shoot()
    
    def stop(self):
        if self.direction == "up":
            self.rect.y -= self.speedy
        if self.direction == "right":
            self.rect.x -= self.speedx
        if self.direction == "down":
            self.rect.y -= self.speedy
        if self.direction == "left":
            self.rect.x -= self.speedx
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            if self.direction == "up":
                x = self.rect.centerx
                y = self.rect.top
            if self.direction == "right":
                x = self.rect.right
                y = self.rect.centery
            if self.direction == "down":
                x = self.rect.centerx
                y = self.rect.bottom
            if self.direction == "left":
                x = self.rect.left
                y = self.rect.centery
            player_bullet = Player_bullet(x, y, self.direction)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        # Показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT 

        self.move()
        
        # Проверка на выход за пределы экрана
        if self.rect.right > WIDTH:
            self.stop()
        if self.rect.left < 0:
            self.stop()
        if self.rect.bottom > HEIGHT:
            self.stop()
        if self.rect.top < 0:
            self.stop()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rand_image = random.choice(enemy_images)
        self.image = self.rand_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([25, WIDTH / 2, WIDTH - 25]) # Генерация случайного места появления
        self.rect.y = 0
        self.direction = "down"
        self.moving_time = 0
        self.moving_time = 3000
        self.last_move = pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 2
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def rotate(self, direction):
        angle = 0
        if direction == "up":
            angle = 180
        elif direction == "right":
            angle = 90
        elif direction == "down":
            angle = 0
        elif direction == "left":
            angle = -90
        new_image = pygame.transform.rotate(self.rand_image, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move > self.moving_time:
            self.last_move = pygame.time.get_ticks()
            self.speedx = 0
            self.speedy = 0
            self.direction = random.choice(["up", "right", "down", "left"])
            self.rotate(self.direction) 
            if self.direction == "up":
                self.speedy = -2
            if self.direction == "right":
                self.speedx = 2
            if self.direction == "down":
                self.speedy = 2
            if self.direction == "left":
                self.speedx = -2
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def stop(self):
        if self.direction == "up":
            self.rect.y -= self.speedy
        if self.direction == "right":
            self.rect.x -= self.speedx
        if self.direction == "down":
            self.rect.y -= self.speedy
        if self.direction == "left":
            self.rect.x -= self.speedx
        self.last_move = 0
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            if self.direction == "up":
                x1 = self.rect.centerx
                y1 = self.rect.top
            if self.direction == "right":
                x1 = self.rect.right
                y1 = self.rect.centery
            if self.direction == "down":
                x1 = self.rect.centerx
                y1 = self.rect.bottom
            if self.direction == "left":
                x1 = self.rect.left
                y1 = self.rect.centery
            enemy_bullet = Enemy_bullet(x1, y1, self.direction)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

    def update(self):
        self.move()
        self.shoot()
        # Проверка на выход за пределы экрана
        if self.rect.right > WIDTH:
            self.stop()
        if self.rect.left < 0:
            self.stop()
        if self.rect.bottom > HEIGHT:
            self.stop()
        if self.rect.top < 0:
            self.stop()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.direction = direction
        self.speedx = 10
        self.speedy = -10
        self.rotate(self.direction)

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


class Player_bullet(Bullet):
    pass
    

class Enemy_bullet(Bullet):
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
        self.type = "life"
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (30 + x, 150 + y)

    def update(self):
        pass


# Загрузка изображений
player_img = pygame.image.load(os.path.join(img_dir, "player_01.png")).convert()
player_img = pygame.transform.scale(player_img, (50, 50))
player_mini_img = pygame.transform.scale(player_img, (25, 25))

enemy_images = []
for i in range(1, 3):
    filename = f"enemy_{i}01.png"
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img = pygame.transform.scale(img, (50, 50))
    img = pygame.transform.rotate(img, 180)
    enemy_images.append(img)

bullet_img = pygame.Surface((8, 16))

explosion_anim = []
for i in range(1, 4):
    filename = f"expl_{i}.png"
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img = pygame.transform.scale(img, (50, 50))
    explosion_anim.append(img)

powerup_images = {}
powerup_images["gun"] = pygame.image.load(os.path.join(img_dir, "powerup_01.png")).convert()
powerup_images["gun"] = pygame.transform.scale(powerup_images["gun"], (40, 40))
powerup_images["shield"] = pygame.image.load(os.path.join(img_dir, "powerup_02.png")).convert()
powerup_images["shield"] = pygame.transform.scale(powerup_images["shield"], (40, 40))
powerup_images["base"] = pygame.image.load(os.path.join(img_dir, "powerup_03.png")).convert()
powerup_images["base"] = pygame.transform.scale(powerup_images["base"], (40, 40))
powerup_images["health"] = pygame.image.load(os.path.join(img_dir, "powerup_04.png")).convert()
powerup_images["health"] = pygame.transform.scale(powerup_images["health"], (40, 40))
powerup_images["life"] = pygame.image.load(os.path.join(img_dir, "powerup_05.png")).convert()
powerup_images["life"] = pygame.transform.scale(powerup_images["life"], (40, 40))
powerup_images["time"] = pygame.image.load(os.path.join(img_dir, "powerup_06.png")).convert()
powerup_images["time"] = pygame.transform.scale(powerup_images["time"], (40, 40))


# Загрузка звуков
game_start_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gamestart.ogg"))
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, "fire.ogg"))
powerup_sound = pygame.mixer.Sound(os.path.join(snd_dir, "powerup.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, "hit.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(snd_dir, "explosion.ogg"))
game_over_sound = pygame.mixer.Sound(os.path.join(snd_dir, "gameover.ogg"))


score = 0
start_time = pygame.time.get_ticks()
game_start_sound.play()
# Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        tiles = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(1):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        # Создание стен
        for i in range(5):
            for j in range(0, 241, 120):
                x = i * 120
                tile = Tile(x, j)
                all_sprites.add(tile)
                tiles.add(tile)

    
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
    

    # Обновление
    all_sprites.update()
    now_time = get_time()

    # Проверка, не столкнулась ли пуля игрока со стеной
    hits = pygame.sprite.groupcollide(tiles, player_bullets, False, True)

    # Проверка, не столкнулась ли пуля противника со стеной
    hits = pygame.sprite.groupcollide(tiles, enemy_bullets, False, True)

    # Проверка, не ударила ли пуля игрока
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.shield -= 25
        if player.shield > 0:
            hit_sound.play()
        else:
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            explosion_sound.play()
        # Если игрок умер, игра окончена
    if player.lives == 0 and not explosion.alive():
        game_over_sound.play()
        game_over = True    

    # Проверка, не ударила ли пуля противника
    hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True) # Учесть ограниченное количество 
    for hit in hits:                                                # появлений противников
        score += 100
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        explosion_sound.play()
        if random.random() > 0.8:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    # Проверка столкновений игрока и улучшений
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        powerup_sound.play()
        if hit.type == "gun":
            pass
        if hit.type == "shield":
            pass
        if hit.type == "base":
            pass
        if hit.type == "health":
            pass
        if hit.type == "life":
            player.lives += 1
            if player.lives >= 3:
                player.lives = 3
        if hit.type == "time":
            pass

    # Проверка, не столкнулся ли игрок со стеной
    if pygame.sprite.spritecollide(player, tiles, False):
        player.stop()
    
    # Проверка, не столкнулся ли противник со стеной
    if pygame.sprite.spritecollide(enemy, tiles, False):
        enemy.stop()

    # Проверка, не столкнулись ли противник и игрок
    if pygame.sprite.collide_rect(player, enemy):
        player.stop()
        enemy.stop()


    # Визуализация (сборка)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, WIDTH / 3 + 25, 5, str(now_time), 24)
    draw_text(screen, WIDTH / 3 * 2 - 25, 5, str(score), 24)
    draw_shield_bar(screen, 5, 10, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
