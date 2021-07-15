import pygame
import random
import config
from classes import EnemyBullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.rand_image = random.choice(config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.direction = "down"
        self.moving_time = 0
        self.moving_time = 3000 # Частота смены направления движения
        self.last_rotate = pygame.time.get_ticks()
        self.speed = config.enemy_speed
        self.speedx = 0
        self.speedy = self.speed
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.life = 100
        self.armor = 0
        self.frozen = False

        config.all_sprites.add(self)
        config.new_enemies.add(self)

    def rotate(self):
        self.direction = random.choice(["up", "right", "down", "left"])
        angle = 0
        if self.direction == "up":
            angle = 180
            self.speedx = 0
            self.speedy = -self.speed
        elif self.direction == "right":
            angle = 90
            self.speedx = self.speed
            self.speedy = 0
        elif self.direction == "down":
            angle = 0
            self.speedx = 0
            self.speedy = self.speed
        elif self.direction == "left":
            angle = -90
            self.speedx = -self.speed
            self.speedy = 0
        new_image = pygame.transform.rotate(self.rand_image, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center    
    
    def reverse(self):
        if self.direction == "up":
            self.direction = "down"
            self.speedy = self.speed
        elif self.direction == "right":
            self.direction = "left"
            self.speedx = -self.speed
        elif self.direction == "down":
            self.direction = "up"
            self.speedy = -self.speed
        elif self.direction == "left":
            self.direction = "right"
            self.speedx = self.speed
        new_image = pygame.transform.rotate(self.image, 180)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):  
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
        self.speedx = 0
        self.speedy = 0
        
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
            enemy_bullet = EnemyBullet(x, y, self.direction, self.bullet_speed, self.bullet_strength)
            config.enemy_bullets.add(enemy_bullet)
            
    def update(self):
        if not self.frozen:
            self.move()
            
            now = pygame.time.get_ticks()
            if now - self.last_rotate > self.moving_time:
                self.last_rotate = pygame.time.get_ticks()
                self.stop()
                self.rotate() 

            # Проверка на выход за пределы экрана
            if (self.rect.right > config.WIDTH or self.rect.left < 0 or
                self.rect.bottom > config.HEIGHT or self.rect.top < 0):
                self.stop()
                self.rotate()
            
            self.shoot()


class NormalEnemy(Enemy):
    def __init__(self, centerx):
        super().__init__(centerx)
        self.rand_image = random.choice(config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0  
        self.tank_type = "normal"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 0
        

class FastEnemy(Enemy):
    def __init__(self, centerx):
        super().__init__(centerx)
        self.rand_image = random.choice(config.enemy_images)[1]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.tank_type = "fast"
        self.speed = config.enemy_speed * 1.4
        self.speedy = self.speed
        self.bullet_speed = 15
        self.bullet_strength = 1
        self.armor = 0

   
class EnhancedEnemy(Enemy):
    def __init__(self, centerx):
        super().__init__(centerx)
        self.rand_image = random.choice(config.enemy_images)[2]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.tank_type = "enhanced"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 50
    

class HeavyEnemy(Enemy):
    def __init__(self, centerx):
        super().__init__(centerx)
        self.rand_image = random.choice(config.enemy_images)[3]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.tank_type = "heavy"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 150
