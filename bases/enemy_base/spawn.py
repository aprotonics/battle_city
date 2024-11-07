import pygame
from configuration import Configuratuion


class Spawn(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = Configuratuion.spawn_images[0]
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

        Configuratuion.all_sprites.add(self)
        Configuratuion.spawns.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame)) # 0 либо 1
            centerx = self.rect.centerx
            self.image = Configuratuion.spawn_images[self.frame]
            self.image.set_colorkey(Configuratuion.BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.y = 0
