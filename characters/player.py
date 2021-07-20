import pygame
import config
from classes import PlayerBullet, Shield


class Player(pygame.sprite.Sprite):    
    def __init__(self, image, level=0, lives=3):
        pygame.sprite.Sprite.__init__(self)
        self.first_image = image
        self.image = self.first_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x,  self.rect.y = config.goal
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y = self.rect.y
        self.direction = "up"

        self.speedx = 0
        self.speedy = 0
        self.sum_x = 0 # Пройденное растояние между точками сетки
        self.sum_y = 0 # Пройденное растояние между точками сетки

        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.bullet_speed = 20
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

        config.all_sprites.add(self)

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
        self.image.set_colorkey(config.BLACK)
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
            self.speedy = -config.player_speed
        elif keystate[pygame.K_RIGHT] == True:
            self.direction = "right"
            self.rotate(self.direction)  
            self.speedx = config.player_speed
        elif keystate[pygame.K_DOWN] == True:
            self.direction = "down"
            self.rotate(self.direction) 
            self.speedy = config.player_speed  
        elif keystate[pygame.K_LEFT] == True:
            self.direction = "left"
            self.rotate(self.direction) 
            self.speedx = -config.player_speed

        self.rect.x += self.speedx
        self.sum_x += self.speedx
        self.rect.y += self.speedy
        self.sum_y += self.speedy 

        # Поиск ближайшей вершины графа
        if self.sum_y <= -50: # движение up
            self.sum_y = -(abs(self.sum_y) % 50)
            self.graph_coordinate_y = self.rect.y - self.sum_y
            self.sum_x = self.rect.x % 50
            self.graph_coordinate_x = self.rect.x - self.sum_x
        if self.sum_x >= 50: # движение right
            self.sum_x = self.sum_x % 50
            self.graph_coordinate_x = self.rect.x - self.sum_x
            self.sum_y = self.rect.y % 50
            self.graph_coordinate_y = self.rect.y - self.sum_y
        if self.sum_y >= 50: # движение down
            self.sum_y = self.sum_y % 50
            self.graph_coordinate_y = self.rect.y - self.sum_y
            self.sum_x = self.rect.x % 50
            self.graph_coordinate_x = self.rect.x - self.sum_x
        if self.sum_x <= -50: # движение left
            self.sum_x = -(abs(self.sum_x) % 50)
            self.graph_coordinate_x = self.rect.x - self.sum_x
            self.sum_y = self.rect.y % 50
            self.graph_coordinate_y = self.rect.y - self.sum_y

        if (keystate[pygame.K_SPACE] == True and
        (config.current_enemy_count > 1 or config.remaining_enemy_count < 2)): # Блокировка стрельбы, если на поле всего 1 противник
            self.shoot()

    def stop(self):
        if self.direction == "up":
            self.rect.y -= self.speedy
            self.sum_y -= self.speedy
        if self.direction == "right":
            self.rect.x -= self.speedx
            self.sum_x -= self.speedx
        if self.direction == "down":
            self.rect.y -= self.speedy
            self.sum_y -= self.speedy
        if self.direction == "left":
            self.rect.x -= self.speedx
            self.sum_x -= self.speedx

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
            player_bullet = PlayerBullet(x, y, self.direction, speed=self.bullet_speed, strength=self.bullet_strength)
            config.player_bullets.add(player_bullet)
            try:
                config.shoot_sound.play()
            except NameError:
                pass

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (config.WIDTH / 2 - 100, config.HEIGHT + 200)

    def upgrade(self, center, direction):
        self.level += 1
        if self.level >= 2:
            self.level = 2
        self.first_image = config.player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(config.BLACK)
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
        self.level = 0
        self.first_image = config.player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.shoot_delay = 500
        self.bullet_speed = 10
        self.armor = 0
        self.bullet_strength = 1

    def player_in_screen(self):
        # Проверка на выход за пределы экрана
        if self.rect.right > config.WIDTH:
            self.stop()
        if self.rect.left <= 0:
            self.stop()
        if self.rect.bottom > config.HEIGHT:
            self.stop()
        if self.rect.top <= 0:
            self.stop()
    
    def player_vs_tiles_colide(self):
        # Проверка столкновений игрока с элементом стены
        hits = pygame.sprite.spritecollide(self, config.tiles, False)
        for hit in hits:
            if hit.type == "STEEL":
                self.stop()
                break
            if hit.type == "BRICK":
                self.stop()
                break
            if hit.type == "GRASS":
                pass
            if hit.type == "WATER":
                self.stop()
                break
            if hit.type == "ICE":
                pass

    def update(self):
        # Показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.image = config.player_images[0]
            self.image.set_colorkey(config.BLACK)
            self.rect = self.image.get_rect()
            self.rect.x,  self.rect.y = config.goal
            self.graph_coordinate_x = self.rect.x
            self.graph_coordinate_y = self.rect.y
            self.direction = "up"
            self.life = 100
            shield = Shield(self.rect.center)
            
            for enemy in config.enemies:
                enemy.mode = 2

        if not self.hidden:
            self.move()
            # Проверка таймера на улучшение стрельбы
            if hasattr(self, "gun_start_time"):
                if pygame.time.get_ticks() - self.gun_start_time > 10000:
                    self.shoot_delay = 500
            
            self.player_in_screen()

            self.player_vs_tiles_colide()
            