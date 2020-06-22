from obj.enemy import Enemy
from obj.projectile import Projectile
from obj.tower import Tower
import pygame


# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 5, 10, 5, pygame.transform.scale(pygame.image.load("sprites/enemies/circle_1.png").convert_alpha(), (20,20)))


class Circle_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 5, 15, 6, pygame.transform.scale(pygame.image.load("sprites/enemies/circle_2.png").convert_alpha(), (25,25)))


class Square_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 4, 25, 7, pygame.transform.scale(pygame.image.load("sprites/enemies/square_1.png").convert_alpha(), (25,25)))


class Square_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 2, 50, 10, pygame.transform.scale(pygame.image.load("sprites/enemies/square_2.png").convert_alpha(), (30,30)))


# Turrets --------------------------------------------------------------------------- #
class Kinetic_1(Tower):
    def __init__(self, pos):
        super().__init__(pos, 5, 250, pygame.image.load("sprites/towers/head/kinetic_1.png"))


class Kinetic_2(Tower):
    def __init__(self, pos):
        super().__init__(pos, 5, 250, pygame.image.load("sprites/towers/head/kinetic_2.png"))


class Kinetic_3(Tower):
    def __init__(self, pos):
        super().__init__(pos, 5, 250, pygame.image.load("sprites/towers/head/kinetic_3.png"))
