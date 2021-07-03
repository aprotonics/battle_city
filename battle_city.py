# Добавлены классы игрока, противника и пули
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] == True:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] == True:
            self.speedx = 5
        if keystate[pygame.K_UP] == True:
            self.speedy = -5
        if keystate[pygame.K_DOWN] == True:
            self.speedy = 5
        if keystate[pygame.K_SPACE] == True:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([25, WIDTH / 2, WIDTH - 25]) # Генерация случайного места появления
        self.rect.y = 0

    def shoot(self): # Стрельба противников
        pass

    def update(self): # Движение противников
        pass


class Bullet(pygame.sprite.Sprite): # Разделить класс на пули игрока и пули противников
    def __init__(self, x, y):             # чтобы не было дружественного огня
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -15
    
    def update(self):
        self.rect.y += self.speedy

        # Убить, если заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


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


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemy = Enemy()
all_sprites.add(enemy)
enemies.add(enemy)


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


    # Визуализация (сборка)
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
