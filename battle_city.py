# Добавлено движение игрока по уровню
import pygame
import random
import os


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


# настройка папки ассетов
img_dir = os.path.join(os.path.dirname(__file__), "img")
snd_dir = os.path.join(os.path.dirname(__file__), "snd")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.direction = "up"
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()    
    
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
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
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
            bullet = Bullet(x, y, self.direction)
            all_sprites.add(bullet)
            bullets.add(bullet)
      
    def update(self):
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
        if keystate[pygame.K_SPACE] == True:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        # Проверка на выход за пределы экрана
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([25, WIDTH / 2, WIDTH - 25]) # Генерация случайного места появления
        self.rect.y = 0



    def shoot(self): # Стрельба противников
        pass

    def update(self): # Движение противников
        pass


class Bullet(pygame.sprite.Sprite): # Разделить класс на пули игрока и пули противников
    def __init__(self, x, y, direction):             # чтобы не было дружественного огня
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speedx = 10
        self.speedy = -10
        self.rotate(self.direction)
    
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
    def update(self):
        pass


class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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
enemy_img = pygame.image.load(os.path.join(img_dir, "enemy_101.png")).convert()
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_img = pygame.transform.rotate(enemy_img, 180)
bullet_img = pygame.Surface((10, 20))


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tiles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
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


# Цикл игры
running = True
while running:
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

    # Проверка, не ударила ли пуля противника
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True) # Учесть ограниченное количество 
    for hit in hits:                                                # появлений противников
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Проверка, не столкнулся ли игрок со стеной
    if pygame.sprite.spritecollide(player, tiles, False):
        player.stop()


    # Визуализация (сборка)
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
