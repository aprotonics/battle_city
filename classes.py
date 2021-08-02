import pygame
import random
from config import Config


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Config.base_images[0]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 600
        self.has_shield = False
        self.shield_duration = 10000
        self.shield_start_time = None
        self.destroyed = False
        self.destroyed_time = None

        self.walls = [  (250, 550), (275, 550), (250, 575), (275, 575),
                        (300, 550), (325, 550), (300, 575), (325, 575),
                        (350, 550), (375, 550), (350, 575), (375, 575),
                        (250, 600), (275, 600), (250, 625), (275, 625),
                        (350, 600), (375, 600), (350, 625), (375, 625),
                    ]

        Config.all_sprites.add(self)

    def clear_wall(self):
        for tile in Config.tiles: 
            if (tile.rect.x, tile.rect.y) in self.walls:
                tile.kill()
    
    def create_wall(self, tile_type: str):
        for element in self.walls:
            x, y = element
            tile = Tile(x, y, tile_type)

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
            self.image = Config.base_images[1]
            self.image.set_colorkey(Config.BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 300
            self.rect.y = 600


class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, direction, owner_id=None, speed=10, strength=1):
        pygame.sprite.Sprite.__init__(self)
        self.owner_id = owner_id
        self.image = Config.bullet_img
        self.image.fill(Config.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.direction = direction
        self.speedx = speed
        self.speedy = -speed
        self.strength = strength
        self.rotate(self.direction)
        
        self.layer = 0

        Config.all_sprites.add(self)
        Config.bullets.add(self)
        Config.layers.add(self)

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
        new_image = pygame.transform.rotate(Config.bullet_img, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.fill(Config.YELLOW)
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
            if self.rect.left > Config.WIDTH:
                self.kill()
        if self.direction == "down":
            self.rect.y -= self.speedy
            if self.rect.top > Config.HEIGHT:
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
        self.image = Config.explosion_anim[0]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120

        self.layer = 0

        Config.all_sprites.add(self)
        Config.layers.add(self)
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Config.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = Config.explosion_anim[self.frame]
                self.image.set_colorkey(Config.BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["gun", "shield", "base", "levelup", "life", "time"])
        self.image = Config.powerup_images[self.type] # ["gun", "shield", "base", "levelup", "life", "time"]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.layer = 0

        Config.all_sprites.add(self)
        Config.powerups.add(self)
        Config.layers.add(self)

    def update(self):
        pass


class Spawn(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = Config.spawn_images[0]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

        Config.all_sprites.add(self)
        Config.spawns.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame)) # 0 либо 1
            centerx = self.rect.centerx
            self.image = Config.spawn_images[self.frame]
            self.image.set_colorkey(Config.BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.y = 0


class Shield(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = Config.shield_images[0]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.spawn_time = pygame.time.get_ticks()
        self.existance_time = 4000

        self.layer = 0

        Config.all_sprites.add(self)
        Config.shields.add(self)
        Config.layers.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.existance_time:
            self.kill()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame))
            self.image = Config.shield_images[self.frame]
            self.image.set_colorkey(Config.BLACK)
            self.rect = self.image.get_rect()
        self.rect.center = Config.player.rect.center


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer = 0
        self.type = tile_type
        self.image = Config.tile_images[self.type]
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y     

        if self.type == "STEEL":
            self.layer = 0
        elif self.type == "BRICK":
            self.layer = 0
        elif self.type == "GRASS":
            self.layer = 1
        elif self.type == "WATER":
            self.subtype = 0
            self.layer = -1
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 120
        elif self.type == "ICE":
            self.layer = -1

        Config.all_sprites.add(self)
        Config.tiles.add(self)
        Config.layers.add(self)

        if self.type != "GRASS" and self.type != "ICE":
            Config.graph.walls.append((x, y))
        
    def update(self):
        if self.type == 'WATER':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.subtype = int(not bool(self.subtype))
                if self.subtype == 1:
                    self.image = Config.tile_images["WATER2"]
                    self.image.set_colorkey(Config.BLACK)   
                if self.subtype == 0:
                    self.image = Config.tile_images["WATER"]
                    self.image.set_colorkey(Config.BLACK)
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
