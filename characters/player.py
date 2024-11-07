import pygame
from configuration import Configuratuion
from classes import PlayerBullet, Shield


n = Configuratuion.n


class Player(pygame.sprite.Sprite):    
    def __init__(self, image, level=0, lives=3):
        pygame.sprite.Sprite.__init__(self)      
        self.first_image = image
        self.image = self.first_image
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x,  self.rect.y = (4 * 50, 12 * 50)
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y = self.rect.y
        self.direction = "up"

        self.speed = Configuratuion.player_speed
        self.speedx = 0
        self.speedy = 0
        self.moving_blocked = False

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

        self.layer = 0

        Configuratuion.all_sprites.add(self)
        Configuratuion.layers.add(self)

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
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):
        keystate = pygame.key.get_pressed()
        if not self.moving_blocked:
            self.speedx = 0
            self.speedy = 0

            # Проверка, какая клавиша нажата. Приоритет UP -> RIGHT -> DOWN -> LEFT
            if keystate[pygame.K_UP] == True:
                self.direction = "up"
                self.rotate(self.direction)
                self.speedy = -self.speed
            elif keystate[pygame.K_RIGHT] == True:
                self.direction = "right"
                self.rotate(self.direction)  
                self.speedx = self.speed
            elif keystate[pygame.K_DOWN] == True:
                self.direction = "down"
                self.rotate(self.direction) 
                self.speedy = self.speed
            elif keystate[pygame.K_LEFT] == True:
                self.direction = "left"
                self.rotate(self.direction) 
                self.speedx = -self.speed

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Поиск ближайшей вершины графа
        x1, y1 = self.rect.x // n * n, self.rect.y // n * n
        x2, y2 = (self.rect.x // n + 1) * n, self.rect.y // n * n
        x3, y3 = self.rect.x // n * n, (self.rect.y // n + 1) * n
        x4, y4 = (self.rect.x // n + 1) * n, (self.rect.y // n + 1) * n
        dist1 = (self.rect.x - x1) ** 2 + (self.rect.y - y1) ** 2
        dist2 = (self.rect.x - x2) ** 2 + (self.rect.y - y2) ** 2
        dist3 = (self.rect.x - x3) ** 2 + (self.rect.y - y3) ** 2
        dist4 = (self.rect.x - x4) ** 2 + (self.rect.y - y4) ** 2
        MAP = {
            dist1: (x1, y1),
            dist2: (x2, y2),
            dist3: (x3, y3),
            dist4: (x4, y4),
        }
        minimum = min(dist1, dist2, dist3, dist4)
        nearest_node = MAP[minimum]
        
        # Если ближайшая вершина изменилась
        if nearest_node[0] != self.graph_coordinate_x or nearest_node[1] != self.graph_coordinate_y:
            self.graph_coordinate_x = nearest_node[0]
            self.graph_coordinate_y = nearest_node[1]

        if (keystate[pygame.K_SPACE] == True and
        (Configuratuion.current_enemy_count > 1 or Configuratuion.remaining_enemy_count < 2)): # Блокировка стрельбы, если на поле всего 1 противник
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
            player_bullet = PlayerBullet(x, y, self.direction, speed=self.bullet_speed, strength=self.bullet_strength)
            Configuratuion.player_bullets.add(player_bullet)
            try:
                Configuratuion.shoot_sound.play()
            except:
                pass

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (Configuratuion.WIDTH / 2 - 100, Configuratuion.HEIGHT + 200)
    
    def show(self):
        self.hidden = False
        self.image = Configuratuion.player_images[0]
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x,  self.rect.y = (4 * 50, 12 * 50)
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y = self.rect.y
        self.direction = "up"
        self.life = 100
        Configuratuion.shield = Shield(self.rect.center)
        
        for enemy in Configuratuion.enemies:
            enemy.mode1_start_time = pygame.time.get_ticks()

    def upgrade(self, center, direction):
        self.level += 1
        if self.level >= 2:
            self.level = 2
        self.first_image = Configuratuion.player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(Configuratuion.BLACK)
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
        self.first_image = Configuratuion.player_images[self.level]
        self.image = self.first_image
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.shoot_delay = 500
        self.bullet_speed = 10
        self.armor = 0
        self.bullet_strength = 1

    def player_in_screen(self):
        # Проверка на выход за пределы экрана
        if self.rect.right > Configuratuion.WIDTH:
            self.stop()
        if self.rect.left <= 0:
            self.stop()
        if self.rect.bottom > Configuratuion.HEIGHT:
            self.stop()
        if self.rect.top <= 0:
            self.stop()
    
    def player_vs_tiles_colide(self):
        # Проверка столкновений игрока с элементом стены
        hits = pygame.sprite.spritecollide(self, Configuratuion.tiles, False)
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
        now = pygame.time.get_ticks()
        
        # Показать, если скрыто
        if self.hidden and now - self.hide_timer > 2000:
            self.show()    

        if not self.hidden:
            self.move()
            
            self.player_in_screen()

            self.player_vs_tiles_colide()
            