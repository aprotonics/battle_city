import pygame


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


class Player(pygame.sprite.Sprite):    
    def __init__(self, image, level=0, lives=3):
        from battle_city import all_sprites, layers

        pygame.sprite.Sprite.__init__(self)
        self.first_image = image
        self.image = self.first_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 100
        self.rect.bottom = HEIGHT
        self.direction = "up"
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.life = 100
        self.armor = 0
        self.lives = lives
        self.level = level
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        if self.level == 1:
            self.shoot_delay = 250
            self.bullet_speed = 15
            self.armor = 50
            self.bullet_strength = 1
        if self.level == 2:
            self.shoot_delay = 250
            self.bullet_speed = 15
            self.armor = 150
            self.bullet_strength = 2

        all_sprites.add(self)
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
        new_image = pygame.transform.rotate(self.first_image, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):
        from battle_city import player_speed, current_enemy_count, remaining_enemy_count

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        # Проверка, какая клавиша нажата. Приоритет UP -> RIGHT -> DOWN -> LEFT
        if keystate[pygame.K_UP] == True:
            self.direction = "up"
            self.rotate(self.direction)
            self.speedy = -player_speed
        elif keystate[pygame.K_RIGHT] == True:
            self.direction = "right"
            self.rotate(self.direction)  
            self.speedx = player_speed
        elif keystate[pygame.K_DOWN] == True:
            self.direction = "down"
            self.rotate(self.direction) 
            self.speedy = player_speed  
        elif keystate[pygame.K_LEFT] == True:
            self.direction = "left"
            self.rotate(self.direction) 
            self.speedx = -player_speed  
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if (keystate[pygame.K_SPACE] == True and
        (current_enemy_count > 1 or remaining_enemy_count < 2)): # Блокировка стрельбы, если на поле всего 1 противник
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
        from battle_city import PlayerBullet, player_bullets, shoot_sound

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
            player_bullet = PlayerBullet(x, y, self.direction, self.bullet_speed, self.bullet_strength)
            player_bullets.add(player_bullet)
            try:
                shoot_sound.play()
            except NameError:
                pass

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2 - 100, HEIGHT + 200)

    def upgrade(self, center, direction):
        from battle_city import player_images

        self.level += 1
        if self.level >= 2:
            self.level = 2
        self.first_image = player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.direction = direction
        self.life = 100
        if self.level == 1:
            self.shoot_delay = 250
            self.bullet_speed = 15
            self.armor = 50
        if self.level == 2:
            self.shoot_delay = 250
            self.bullet_speed = 15
            self.armor = 150
            self.bullet_strength = 2
        self.rotate(direction)

    def downgrade(self, center):
        from battle_city import player_images

        self.level = 0
        self.first_image = player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.shoot_delay = 500
        self.bullet_speed = 10
        self.armor = 0
        self.bullet_strength = 1

    def update(self):
        from battle_city import player_images, Shield

        # Показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.image = player_images[0]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2 - 100
            self.rect.bottom = HEIGHT
            self.direction = "up"
            self.life = 100
            shield = Shield(self.rect.center)

        if not self.hidden:
            self.move()
            # Проверка таймера на улучшение стрельбы
            if hasattr(self, "gun_start_time"):
                if pygame.time.get_ticks() - self.gun_start_time > 10000:
                    self.shoot_delay = 400
            # Проверка на выход за пределы экрана
            if self.rect.right > WIDTH:
                self.stop()
            if self.rect.left < 0:
                self.stop()
            if self.rect.bottom > HEIGHT:
                self.stop()
            if self.rect.top < 0:
                self.stop()
