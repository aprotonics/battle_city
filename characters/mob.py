import pygame
import random
import datetime
from config import Config
from structures import PriorityQueue
from classes import EnemyBullet


def create_path(start, goal):
    start_time = datetime.datetime.now()

    came_from, cost_so_far, iterations = a_star_search(Config.graph, start, goal)

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


n = Config.n


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_id, x):
        pygame.sprite.Sprite.__init__(self)
        self.ice_count = 0
        self.id = enemy_id
        self.spawn_x = x
        self.mode = 1
        self.mode1_start_time = pygame.time.get_ticks()
        self.mode1_duration = Config.enemy_mode1_duration
        self.rand_image = random.choice(Config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.spawn_x
        self.rect.y = 0
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y =  self.rect.y

        self.direction = "down"
        self.moving_time = 0
        self.moving_time = 3000 # Частота смены направления движения
        self.last_rotate = pygame.time.get_ticks()
        self.speed = Config.enemy_speed
        self.speedx = 0
        self.speedy = self.speed
        self.moving_radius = 50

        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.bullet_speed = 5
        self.bullet_strength = 1
        self.life = 100
        self.armor = 0
        self.frozen = False

        self.layer = 0

        Config.all_sprites.add(self)
        Config.new_enemies.add(self)
        Config.layers.add(self)

    def __init_mode2__(self):
        self.mode = 2
        self.mode2_start_time = pygame.time.get_ticks()
        self.mode2_duration = Config.enemy_mode2_duration
        self.rect.x = round(self.rect.x / n) * n
        self.rect.y = round(self.rect.y / n) * n
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y =  self.rect.y

        self.start = (self.graph_coordinate_x, self.graph_coordinate_y)
        self.step = 0
        self.goal = (Config.player.graph_coordinate_x, Config.player.graph_coordinate_y)
        print(self.start)
        print(self.goal)
        self.path_to_player = create_path(self.start, self.goal)
        self.current_position = self.path_to_player[self.step]
        print(f"{self.id}.{self.step}. {self.current_position}")
        if len(self.path_to_player) > 1:
            self.next_position = self.path_to_player[self.step + 1]
        self.path_update_delay = 3000
        self.path_update_time = pygame.time.get_ticks()

        self.moving_blocked = False
        self.moving_blocked_time = None
        self.timeout = 4000
        self.occupied_points = set()

        Config.enemies_mode1.remove(self)
        Config.enemies_mode2.add(self)
    
    def __init_mode3__(self):
        self.mode = 3
        self.rect.x = round(self.rect.x / n) * n
        self.rect.y = round(self.rect.y / n) * n
        self.graph_coordinate_x = self.rect.x
        self.graph_coordinate_y =  self.rect.y

        self.start = (self.graph_coordinate_x, self.graph_coordinate_y)
        self.step = 0
        self.goal1 = (Config.base.rect.x - 100, Config.base.rect.y)
        self.goal2 = (Config.base.rect.x, Config.base.rect.y - 100)
        self.goal3 = (Config.base.rect.x + 100, Config.base.rect.y)
        self.path_to_base, self.goal = self.get_min_path_to_base()

        print(self.start)
        print(self.goal)

        self.current_position = self.path_to_base[self.step]
        print(f"{self.id}.{self.step}. {self.current_position}")
        if self.step < len(self.path_to_base) - 1:
            self.next_position = self.path_to_base[self.step + 1]
        self.path_update_delay = float("inf")
        self.path_update_time = pygame.time.get_ticks()
    
        self.moving_blocked = False
        self.moving_blocked_time = None

        Config.enemies_mode2.remove(self)
        Config.enemies_mode3.add(self)
       
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
        self.image.set_colorkey(Config.BLACK)
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
        self.image.set_colorkey(Config.BLACK)
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
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def move(self):  # Добавить
        self.speedx = 0
        self.speedy = 0

        if self.direction == "up":
            self.speedx = 0
            self.speedy = -self.speed
        elif self.direction == "right":
            self.speedx = self.speed
            self.speedy = 0
        elif self.direction == "down":
            self.speedx = 0
            self.speedy = self.speed
        elif self.direction == "left":
            self.speedx = -self.speed
            self.speedy = 0
        
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
    
    def move_mode2(self):
        self.speedx = 0
        self.speedy = 0
     
        # Определение направления движения
        if self.next_position[1] - self.current_position[1] == n:
            self.direction = "down"
            self.rotate_mode2(self.direction)
            self.speedy = self.speed
        elif self.next_position[1] - self.current_position[1] == -n:
            self.direction = "up"
            self.rotate_mode2(self.direction)
            self.speedy = -self.speed
        elif self.next_position[0] - self.current_position[0] == n:
            self.direction = "right"
            self.rotate_mode2(self.direction)
            self.speedx = self.speed
        elif self.next_position[0] - self.current_position[0] == -n:
            self.direction = "left"
            self.rotate_mode2(self.direction)
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
            self.set_free_graph_coordinates()
            self.graph_coordinate_x = nearest_node[0]
            self.graph_coordinate_y = nearest_node[1]
            self.set_occupied_graph_coordinates()

        # Проверка на преодоление следующей точки пути !Проверить на необходимость!!!
        if self.direction == "down":
            if self.rect.y > self.next_position[1]:
                self.rect.y = self.next_position[1]
        elif self.direction == "up":
            if self.rect.y < self.next_position[1]:
                self.rect.y = self.next_position[1]
        elif self.direction == "right":
            if self.rect.x > self.next_position[0]:
                self.rect.x = self.next_position[0]
        elif self.direction == "left":
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

    def update_path(self, start, goal): 
        print(start, goal)
        self.path_to_player = create_path(start, goal) 
        print("path", self.path_to_player)  
        self.step = 0
        self.current_position = self.path_to_player[self.step]
        if len(self.path_to_player) > 1:
            self.next_position = self.path_to_player[self.step + 1]
    
    def get_min_path_to_base(self):
        path_to_base1 = create_path(self.start, self.goal1)
        path_to_base2 = create_path(self.start, self.goal2)
        path_to_base3 = create_path(self.start, self.goal3)
        
        min_len_path_to_base = min(len(path_to_base1), len(path_to_base2), len(path_to_base3))
        
        if len(path_to_base1) == min_len_path_to_base:
            goal =  self.goal1
            path_to_base = path_to_base1
        elif len(path_to_base2) == min_len_path_to_base:
            goal =  self.goal2
            path_to_base = path_to_base2
        elif len(path_to_base3) == min_len_path_to_base:
            goal =  self.goal3
            path_to_base = path_to_base1
        
        return path_to_base, goal
    
    def change_next_position(self, path):
        if self.current_position != self.next_position:
            self.step += 1
            self.current_position = self.next_position 
            print(f"{self.id}.{self.step}. {self.current_position}")       
            if self.step < len(path) - 1:
                self.next_position = path[self.step + 1]
    
    def reset_mode2_properties(self):
        delattr(self, "mode2_start_time")
        delattr(self, "mode2_duration")
        delattr(self, "start")
        delattr(self, "step")
        delattr(self, "goal")
        delattr(self, "path_to_player")
        delattr(self, "current_position")
        delattr(self, "next_position")
        delattr(self, "path_update_delay")
        delattr(self, "path_update_time")
        delattr(self, "moving_blocked")
        delattr(self, "moving_blocked_time")
        delattr(self, "timeout")
        delattr(self, "occupied_points")
    
    def reset_mode3_properties(self):
        delattr(self, "path_to_base")
        delattr(self, "goal1")
        delattr(self, "goal2")
        delattr(self, "goal3")

    def change_mode(self, from_mode, to_mode): # Дописать
        if to_mode == 2:
            self.__init_mode2__()
        if to_mode == 3:
            self.__init_mode3__()
        if to_mode == 1 and from_mode == 2:
            self.reset_mode2_properties()      
            self.mode = 1
            self.mode1_start_time = pygame.time.get_ticks()
            self.mode1_duration = Config.enemy_mode1_duration
            Config.enemies_mode2.remove(self)
            Config.enemies_mode1.add(self)
        if to_mode == 1 and from_mode == 3:
            self.reset_mode3_properties()
            self.reset_mode2_properties()  
            self.mode = 1
            self.mode1_start_time = pygame.time.get_ticks()
            self.mode1_duration = Config.enemy_mode1_duration
            Config.enemies_mode3.remove(self)
            Config.enemies_mode1.add(self)

    def set_free_graph_coordinates(self):
        x, y = (self.graph_coordinate_x, self.graph_coordinate_y)
        if (x, y) in self.occupied_points:
            self.occupied_points.remove((x, y))

        radius = self.moving_radius
        points_into_radius = [(x + i, y + j) for i in range(-radius, radius+1, 25)
                                for j in range(-radius, radius+1, 25)]
        
        for point in points_into_radius:
            if point in self.occupied_points:
                self.occupied_points.remove(point)

    def set_occupied_graph_coordinates(self):
        # Проверка на наличие занимаемой точки пути в путях других противников
        x, y = (self.graph_coordinate_x, self.graph_coordinate_y)
        self.occupied_points.add((x, y))

        radius = self.moving_radius
        points_into_radius = [(x + i, y + j) for i in range(-radius, radius+1, 25)
                                for j in range(-radius, radius+1, 25)]
        
        for point in points_into_radius:
            self.occupied_points.add(point)
    
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
            enemy_bullet = EnemyBullet(x, y, self.direction, owner_id=self.id, speed=self.bullet_speed, strength=self.bullet_strength)
            Config.enemy_bullets.add(enemy_bullet)

    def update(self):
        if not self.frozen:
            now = pygame.time.get_ticks()
            
            # Смена режима после появления
            # From 1 to 2
            if (self.mode == 1 and Config.player.hidden == False and
                now - self.mode1_start_time > self.mode1_duration):
                self.change_mode(1, 2)
            # From 2 to 3
            if (self.mode == 2 and Config.base.destroyed == False and
                now - self.mode2_start_time > self.mode2_duration):
                self.change_mode(2, 3)
        
            if self.mode == 1: # Режим №1
                self.move()
                
                # Если прошла задержка, повернуться
                if now - self.last_rotate > self.moving_time:
                    self.last_rotate = pygame.time.get_ticks()
                    self.stop()
                    self.rotate() 

                # Проверка на выход за пределы экрана
                if (self.rect.right > Config.WIDTH or self.rect.left < 0 or
                    self.rect.bottom > Config.HEIGHT or self.rect.top < 0):
                    self.stop()
                    self.rotate()

            elif self.mode == 2: # Режим №2
                # Если точка пути достигнута, перейти к следующей
                if self.rect.x == self.next_position[0] and self.rect.y == self.next_position[1]:
                    self.change_next_position(self.path_to_player)
                
                # Если прошла задержка, обновить путь
                if now - self.path_update_time > self.path_update_delay:
                    self.path_update_time = now
                    self.start = (self.current_position[0], self.current_position[1])
                    self.goal = (Config.player.graph_coordinate_x, Config.player.graph_coordinate_y)
                    self.update_path(self.start, self.goal)

                # Если путь пройден, запросить новый путь
                if self.current_position == self.next_position:
                    self.path_update_time = now
                    self.start = (self.current_position[0], self.current_position[1])
                    self.goal = (Config.player.graph_coordinate_x, Config.player.graph_coordinate_y)
                    self.update_path(self.start, self.goal)
                    self.current_position = self.path_to_player[self.step]
                    if len(self.path_to_player) > 1:
                        self.next_position = self.path_to_player[self.step + 1]
                
                # Если следующая точка пути не занята, продолжить движение
                self.remove(Config.enemies_mode2)
                for enemy in Config.enemies_mode2:
                    if len(self.path_to_player) > 1: # Проверка на длину пути
                        if self.path_to_player[self.step + 1] in enemy.occupied_points:
                            if not self.moving_blocked:
                                self.moving_blocked = True
                                self.moving_blocked_time = now
                            break
                else:
                    self.moving_blocked = False
                self.add(Config.enemies_mode2)

                if not self.moving_blocked:
                    self.move_mode2()
            
            elif self.mode == 3: # Режим №3
                # Если точка пути достигнута, перейти к следующей
                if self.rect.x == self.next_position[0] and self.rect.y == self.next_position[1]:
                    self.change_next_position(self.path_to_base)

                # Если путь не пройден и следующая точка пути не занята, продолжить движение
                if self.current_position != self.next_position:
                    self.remove(Config.enemies_mode3)
                    for enemy in Config.enemies_mode3:
                        if self.path_to_base[self.step + 1] in enemy.occupied_points:
                            self.moving_blocked = True
                            self.moving_blocked_time = now
                            break
                    else:
                        self.moving_blocked = False
                    self.add(Config.enemies_mode3)
                    
                    if not self.moving_blocked:
                        self.move_mode2()
                
                # Если путь пройден, повернуться к базе
                if self.current_position == self.next_position:
                    if self.rect.x < Config.base.rect.x:
                        self.direction = "right"
                    elif self.rect.y < Config.base.rect.y:
                        self.direction = "down"
                    elif self.rect.x > Config.base.rect.x:
                        self.direction = "left"

                    self.rotate_mode2(self.direction)

            self.shoot()


class NormalEnemy(Enemy):
    def __init__(self, enemy_id, x):
        super().__init__(enemy_id, x)
        self.rand_image = random.choice(Config.enemy_images)[0]
        self.image = self.rand_image
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0  
        self.tank_type = "normal"
        self.speed = Config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 5
        self.bullet_strength = 1
        self.armor = 0
        

class FastEnemy(Enemy):
    def __init__(self, enemy_id, x):
        super().__init__(enemy_id, x)
        self.rand_image = random.choice(Config.enemy_images)[1]
        self.image = self.rand_image
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "fast"
        self.speed = Config.enemy_speed * 1.4
        self.speedy = self.speed
        self.bullet_speed = 15
        self.bullet_strength = 1
        self.armor = 0

   
class EnhancedEnemy(Enemy):
    def __init__(self, enemy_id, x):
        super().__init__(enemy_id, x)
        self.rand_image = random.choice(Config.enemy_images)[2]
        self.image = self.rand_image
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "enhanced"
        self.speed = Config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 50
    

class HeavyEnemy(Enemy):
    def __init__(self, enemy_id, x):
        super().__init__(enemy_id, x)
        self.rand_image = random.choice(Config.enemy_images)[3]
        self.image = self.rand_image
        self.image.set_colorkey(Config.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.tank_type = "heavy"
        self.speed = Config.enemy_speed
        self.speedy = self.speed
        self.bullet_speed = 10
        self.bullet_strength = 1
        self.armor = 150
