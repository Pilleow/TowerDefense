from obj.enemy import Enemy
from obj.projectile import Projectile
from obj.tower import Tower
import pygame

pygame.init()
Screen = pygame.display.set_mode((800,600))

enemy_imgs = [
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_1.png").convert_alpha(), (20,20)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_2.png").convert_alpha(), (25,25)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_1.png").convert_alpha(), (30,30)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_2.png").convert_alpha(), (40,40)),
]

turret_imgs = [pygame.image.load(f"sprites/towers/head/kinetic_{x}.png").convert_alpha() for x in range(1,4)]

# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 25, 5, 5, 10, enemy_imgs[0])


class Circle_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 32, 10, 6, 20, enemy_imgs[1])


class Square_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 40, 15, 7, 25, enemy_imgs[2])


class Square_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 50, 20, 10, 50, enemy_imgs[3])


# Turrets --------------------------------------------------------------------------- #
class Kinetic_1(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 125
        else:
            range_ = 0
        super().__init__(pos, 5, 250, turret_imgs[0], level, range_, 60)


class Kinetic_2(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 175
        else:
            range_ = 0
        super().__init__(pos, 5, 500, turret_imgs[1], level, range_, 60)


class Kinetic_3(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 175
        else:
            range_ = 0
        super().__init__(pos, 10, 750, turret_imgs[2], level, range_, 60)
