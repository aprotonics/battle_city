import pygame
import random
import config


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = config.base_images[0]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 600
        self.has_shield = False
        self.shield_duration = 10000
        self.shield_start_time = None
        self.destroyed = False
        self.destroyed_time = None

        config.all_sprites.add(self)

    def clear_wall(self):
        for tile in config.tiles: 
            if (5 * 50 <= tile.rect.x < 6 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                6 * 50 <= tile.rect.x < 7 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                7 * 50 <= tile.rect.x < 8 * 50 and 11 * 50 <= tile.rect.y < 12 * 50 or
                5 * 50 <= tile.rect.x < 6 * 50 and 12 * 50 <= tile.rect.y < 13 * 50 or
                7 * 50 <= tile.rect.x < 8 * 50 and 12 * 50 <= tile.rect.y < 13 * 50):
                tile.kill()
    
    def create_wall(self, tile_type: str):
        x_left = config.base.rect.x - 50

        # Создание трёх верхних блоков
        for i in range(3):  
            tile = Tile(x_left + i * 50, config.base.rect.y - 50, tile_type)
            tile = Tile(x_left + 25 + i * 50, config.base.rect.y - 50, tile_type)
            tile = Tile(x_left + i * 50, config.base.rect.y - 25, tile_type)
            tile = Tile(x_left + 25 + i * 50, config.base.rect.y - 25, tile_type)

        # Создание двух боковых блоков
        for i in range(2):
            tile = Tile(x_left + i * 100, config.base.rect.y, tile_type)
            tile = Tile(x_left + 25 + i * 100, config.base.rect.y, tile_type)
            tile = Tile(x_left + i * 100, config.base.rect.y + 25, tile_type)
            tile = Tile(x_left + 25 + i * 100, config.base.rect.y + 25, tile_type)

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
            now = pygame.time.get_ticks()
            if now - self.shield_start_time > self.shield_duration:
                self.shield_start_time = None
                self.downgrade_wall()
        
        if self.destroyed:
            self.image = config.base_images[1]
            self.image.set_colorkey(config.BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 300
            self.rect.y = 600


class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, direction, speed=10, strength=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = config.bullet_img
        self.image.fill(config.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.direction = direction
        self.speedx = speed
        self.speedy = -speed
        self.strength = strength
        self.rotate(self.direction)
        
        config.all_sprites.add(self)
        config.bullets.add(self)
        config.layers.add(self)

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
        new_image = pygame.transform.rotate(config.bullet_img, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.fill(config.YELLOW)
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
            if self.rect.left > config.WIDTH:
                self.kill()
        if self.direction == "down":
            self.rect.y -= self.speedy
            if self.rect.top > config.HEIGHT:
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
        self.image = config.explosion_anim[0]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120

        config.all_sprites.add(self)
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(config.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = config.explosion_anim[self.frame]
                self.image.set_colorkey(config.BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["gun", "shield", "base", "levelup", "life", "time"])
        self.image = config.powerup_images[self.type] # ["gun", "shield", "base", "levelup", "life", "time"]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

        config.all_sprites.add(self)
        config.powerups.add(self)

    def update(self):
        pass


class Spawn(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = config.spawn_images[0]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

        config.all_sprites.add(self)
        config.spawns.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame)) # 0 либо 1
            centerx = self.rect.centerx
            self.image = config.spawn_images[self.frame]
            self.image.set_colorkey(config.BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.y = 0


class Shield(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = config.shield_images[0]
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.spawn_time = pygame.time.get_ticks()
        self.existance_time = 4000

        config.all_sprites.add(self)
        config.shields.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.existance_time:
            self.kill()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame))
            self.image = config.shield_images[self.frame]
            self.image.set_colorkey(config.BLACK)
            self.rect = self.image.get_rect()
        self.rect.center = config.player.rect.center


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer = 0
        self.type = tile_type
        self.image = config.tile_images[self.type]
        self.image.set_colorkey(config.BLACK)
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

        config.all_sprites.add(self)
        config.tiles.add(self)
        config.layers.add(self)
        
    def update(self):
        if self.type == 'WATER':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.subtype = int(not bool(self.subtype))
                if self.subtype == 1:
                    self.image = config.tile_images["WATER2"]
                    self.image.set_colorkey(config.BLACK)   
                if self.subtype == 0:
                    self.image = config.tile_images["WATER"]
                    self.image.set_colorkey(config.BLACK)
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
