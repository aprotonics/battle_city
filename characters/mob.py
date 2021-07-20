import pygame
import random
import datetime
import config
from structures import PriorityQueue
from classes import EnemyBullet


def create_path(start, goal):
    start_time = datetime.datetime.now()

    came_from, cost_so_far, iterations = a_star_search(config.graph, start, goal)

    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()

    end_time = datetime.datetime.now()
    print("time", end_time - start_time)
    print("iterations", iterations)

    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    iterations = 0
    frontier = PriorityQueue() # Граница
    frontier.push(start, 0)
    came_from = {} # Откуда пришли
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    # Обход графа
    while not frontier.empty():
        current = frontier.extract()

        if current == goal:
            break

        for element in graph.neighbours(current):
            iterations += 1
            new_cost = cost_so_far[current] + graph.cost(current, element)
            if element not in cost_so_far or new_cost < cost_so_far[element]:
                cost_so_far[element] = new_cost
                priority = new_cost + heuristic(goal, element)
                frontier.push(element, priority)
                came_from[element] = current
    
    return came_from, cost_so_far, iterations


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_time = pygame.time.get_ticks()
        self.mode = 1
        self.mode1_duration = 5000
        self.rand_image = random.choice(config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

        self.direction = "down"
        self.moving_time = 0
        self.moving_time = 3000 # Частота смены направления движения
        self.last_rotate = pygame.time.get_ticks()
        self.speed = config.enemy_speed
        self.speedx = 0
        self.speedy = self.speed

        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.bullet_speed = 5
        self.bullet_strength = 1
        self.life = 100
        self.armor = 0
        self.frozen = False

        config.all_sprites.add(self)
        config.new_enemies.add(self)

    def __init_mode2__(self):
        self.mode = 2
        self.rect.x = round(self.rect.x / 50) * 50
        self.rect.y = round(self.rect.y / 50) * 50
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y =  self.rect.y

        self.start = (self.graph_coordinate_x, self.graph_coordinate_y)
        self.step = 0
        self.goal = (config.player.graph_coordinate_x, config.player.graph_coordinate_y)
        print(self.start)
        print(self.goal)
        self.path_to_player = create_path(self.start, self.goal)
        self.current_position = self.path_to_player[self.step]
        print(f"{self.step}. {self.current_position}")
        self.next_position = self.path_to_player[self.step + 1]
        self.path_update_delay = 3000
        self.path_update_time = pygame.time.get_ticks()
       
    def rotate(self):
        self.direction = random.choice(["up", "right", "down", "left"])
        angle = 0
        if self.direction == "up":
            angle = 180
            self.speedx = 0
            self.speedy = -self.speed
        elif self.direction == "right":
            angle = 90
            self.speedx = self.speed
            self.speedy = 0
        elif self.direction == "down":
            angle = 0
            self.speedx = 0
            self.speedy = self.speed
        elif self.direction == "left":
            angle = -90
            self.speedx = -self.speed
            self.speedy = 0
        new_image = pygame.transform.rotate(self.rand_image, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def rotate_mode2(self, direction):
        angle = 0
        if direction == "up":
            angle = 180
        elif direction == "right":
            angle = 90
        elif direction == "down":
            angle = 0
        elif direction == "left":
            angle = -90
        new_image = pygame.transform.rotate(self.rand_image, angle)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def reverse(self):
        if self.direction == "up":
            self.direction = "down"
            self.speedy = self.speed
        elif self.direction == "right":
            self.direction = "left"
            self.speedx = -self.speed
        elif self.direction == "down":
            self.direction = "up"
            self.speedy = -self.speed
        elif self.direction == "left":
            self.direction = "right"
            self.speedx = self.speed
        new_image = pygame.transform.rotate(self.image, 180)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):  
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    
    def move_mode2(self):
        self.speedx = 0
        self.speedy = 0
     
        # Определение направления движения
        if self.next_position[1] - self.current_position[1] == 25:
            self.direction = "down"
            self.rotate_mode2(self.direction)
            self.speedy = self.speed
        elif self.next_position[1] - self.current_position[1] == -25:
            self.direction = "up"
            self.rotate_mode2(self.direction)
            self.speedy = -self.speed
        elif self.next_position[0] - self.current_position[0] == 25:
            self.direction = "right"
            self.rotate_mode2(self.direction)
            self.speedx = self.speed
        elif self.next_position[0] - self.current_position[0] == -25:
            self.direction = "left"
            self.rotate_mode2(self.direction)
            self.speedx = -self.speed 

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Проверка на преодоление следующей точки пути
        if self.direction == "down":
            if self.rect.y > self.next_position[1]:
                self.rect.y = self.next_position[1]
        if self.direction == "up":
            if self.rect.y < self.next_position[1]:
                self.rect.y = self.next_position[1]
        if self.direction == "right":
            if self.rect.x > self.next_position[0]:
                self.rect.x = self.next_position[0]
        if self.direction == "left":
            if self.rect.x < self.next_position[0]:
                self.rect.x = self.next_position[0]

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
            enemy_bullet = EnemyBullet(x, y, self.direction, speed=self.bullet_speed, strength=self.bullet_strength)
            config.enemy_bullets.add(enemy_bullet)

    def update_path(self, start, goal): 
        print(start, goal)
        self.path_to_player = create_path(start, goal) 
        print("path", self.path_to_player)  
        self.step = 0
    
    def change_positions(self):
        if self.current_position != self.next_position:
            self.step += 1
            self.current_position = self.next_position 
            print(f"{self.step}. {self.current_position}")       
            if self.step < len(self.path_to_player) - 1:
                self.next_position = self.path_to_player[self.step + 1]
    
    def change_mode(self, from_mode, to_mode):
        self.__init_mode2__()
        # self.mode = to_mode

    def update(self):
        now = pygame.time.get_ticks()
        if self.mode == 1 and now - self.spawn_time > self.mode1_duration:
            self.change_mode(1, 2)

        if not self.frozen:
            if self.mode == 1: # Режим №1
                self.move()
                
                if now - self.last_rotate > self.moving_time:
                    self.last_rotate = pygame.time.get_ticks()
                    self.stop()
                    self.rotate() 

                # Проверка на выход за пределы экрана
                if (self.rect.right > config.WIDTH or self.rect.left < 0 or
                    self.rect.bottom > config.HEIGHT or self.rect.top < 0):
                    self.stop()
                    self.rotate()

            elif self.mode == 2: # Режим №2
                # Если прошла задержка, обновить путь
                if now - self.path_update_time > self.path_update_delay:
                    self.path_update_time = now
                    self.start = (self.current_position[0], self.current_position[1])
                    self.goal = (config.player.graph_coordinate_x, config.player.graph_coordinate_y)
                    self.update_path(self.start, self.goal)
                    # print("path_to_player", self.path_to_player)
                    # print("coordinates", (self.rect.x, self.rect.y))
                
                # Если точка пути достигнута, перейти к следующей
                if self.rect.x == self.next_position[0] and self.rect.y == self.next_position[1]:
                    self.change_positions()

                # Если путь пройден, запросить новый путь
                if self.current_position == self.next_position:
                    self.path_update_time = now
                    self.start = (self.current_position[0], self.current_position[1])
                    self.goal = (config.player.graph_coordinate_x, config.player.graph_coordinate_y)
                    self.update_path(self.start, self.goal)
                    self.current_position = self.path_to_player[self.step]
                    if self.step < len(self.path_to_player) - 1:
                        self.next_position = self.path_to_player[self.step + 1]
                
                self.move_mode2()

            self.shoot()


class NormalEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x)
        self.rand_image = random.choice(config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0  
        self.tank_type = "normal"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 5
        self.bullet_strength = 1
        self.armor = 0
        

class FastEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x)
        self.rand_image = random.choice(config.enemy_images)[1]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "fast"
        self.speed = config.enemy_speed * 1.4
        self.speedy = self.speed
        self.bullet_speed = 15
        self.bullet_strength = 1
        self.armor = 0

   
class EnhancedEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x)
        self.rand_image = random.choice(config.enemy_images)[2]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "enhanced"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 50
    

class HeavyEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x)
        self.rand_image = random.choice(config.enemy_images)[3]
        self.image = self.rand_image
        self.image.set_colorkey(config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "heavy"
        self.speed = config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 150
