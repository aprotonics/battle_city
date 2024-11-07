import pygame
from configuration import Configuratuion


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = Configuratuion.explosion_anim[0]
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120

        self.layer = 0

        Configuratuion.all_sprites.add(self)
        Configuratuion.layers.add(self)
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(Configuratuion.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = Configuratuion.explosion_anim[self.frame]
                self.image.set_colorkey(Configuratuion.BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center
