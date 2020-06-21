from obj.enemy import Enemy
from obj.projectile import Projectile
from obj.tower import Tower
import pygame

# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 5, 10, 5, pygame.image.load("sprites/enemies/circle_1.png").convert_alpha())


class Circle_2(Enemy):
    def __init__(self):
        super().__init__(start, 5, 10, 5, pygame.image.load("sprites/enemies/circle_2.png").convert_alpha())


class Square_1(Enemy):
    def __init__(self):
        super().__init__(start, 5, 10, 5, pygame.image.load("sprites/enemies/square_1.png").convert_alpha())


class Square_2(Enemy):
    def __init__(self):
        super().__init__(start, 5, 10, 5, pygame.image.load("sprites/enemies/square_2.png").convert_alpha())


# Turrets --------------------------------------------------------------------------- #

