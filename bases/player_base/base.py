import pygame
from configuration import Configuratuion


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Configuratuion.base_images[0]
        self.image.set_colorkey(Configuratuion.BLACK)
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

        Configuratuion.all_sprites.add(self)

    def clear_wall(self):
        for tile in Configuratuion.tiles: 
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
            self.image = Configuratuion.base_images[1]
            self.image.set_colorkey(Configuratuion.BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 300
            self.rect.y = 600


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer = 0
        self.type = tile_type
        self.image = Configuratuion.tile_images[self.type]
        self.image.set_colorkey(Configuratuion.BLACK)
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

        Configuratuion.all_sprites.add(self)
        Configuratuion.tiles.add(self)
        Configuratuion.layers.add(self)

        if self.type != "GRASS" and self.type != "ICE":
            Configuratuion.graph.walls.append((x, y))
        
    def update(self):
        if self.type == 'WATER':
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.subtype = int(not bool(self.subtype))
                if self.subtype == 1:
                    self.image = Configuratuion.tile_images["WATER2"]
                    self.image.set_colorkey(Configuratuion.BLACK)   
                if self.subtype == 0:
                    self.image = Configuratuion.tile_images["WATER"]
                    self.image.set_colorkey(Configuratuion.BLACK)
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
