from obj.enemy import Enemy
from obj.projectile import Projectile
from obj.tower import Tower
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()


# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 7, 10, 5, pygame.transform.scale(pygame.image.load("sprites/enemies/circle_1.png").convert_alpha(), (20,20)))


class Circle_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 6, 10, 6, pygame.transform.scale(pygame.image.load("sprites/enemies/circle_2.png").convert_alpha(), (25,25)))


class Square_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 5, 10, 7, pygame.transform.scale(pygame.image.load("sprites/enemies/square_1.png").convert_alpha(), (25,25)))


class Square_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 4, 10, 8, pygame.transform.scale(pygame.image.load("sprites/enemies/square_2.png").convert_alpha(), (30,30)))


# Turrets --------------------------------------------------------------------------- #

