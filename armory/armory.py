import pygame
from configuration import Configuratuion


class Bullet(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, direction, owner_id=None, speed=10, strength=1):
        pygame.sprite.Sprite.__init__(self)
        self.owner_id = owner_id
        self.image = Configuratuion.bullet_img
        self.image.fill(Configuratuion.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.direction = direction
        self.speedx = speed
        self.speedy = -speed
        self.strength = strength
        self.rotate(self.direction)
        
        self.layer = 0

        Configuratuion.all_sprites.add(self)
        Configuratuion.bullets.add(self)
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
        new_image = pygame.transform.rotate(Configuratuion.bullet_img, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.fill(Configuratuion.YELLOW)
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
            if self.rect.left > Configuratuion.WIDTH:
                self.kill()
        if self.direction == "down":
            self.rect.y -= self.speedy
            if self.rect.top > Configuratuion.HEIGHT:
                self.kill()
        if self.direction == "left":
            self.rect.x -= self.speedx
            if self.rect.right < 0:
                self.kill()


class PlayerBullet(Bullet):
    pass
        

class EnemyBullet(Bullet):
    pass


class Shield(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = Configuratuion.shield_images[0]
        self.image.set_colorkey(Configuratuion.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.spawn_time = pygame.time.get_ticks()
        self.existance_time = 4000

        self.layer = 0

        Configuratuion.all_sprites.add(self)
        Configuratuion.shields.add(self)
        Configuratuion.layers.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.existance_time:
            self.kill()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = int(not bool(self.frame))
            self.image = Configuratuion.shield_images[self.frame]
            self.image.set_colorkey(Configuratuion.BLACK)
            self.rect = self.image.get_rect()
        self.rect.center = Configuratuion.player.rect.center
