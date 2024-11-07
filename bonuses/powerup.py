import pygame
import random
from configuration import Configuratuion


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["gun", "shield", "base", "levelup", "life", "time"])
        self.image = Configuratuion.powerup_images[self.type] # ["gun", "shield", "base", "levelup", "life", "time"]
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.layer = 0

        Configuratuion.all_sprites.add(self)
        Configuratuion.powerups.add(self)
        Configuratuion.layers.add(self)

    def update(self):
        pass
