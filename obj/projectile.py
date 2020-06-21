import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()


class Projectile:
    def __init__(self, v, pos, dmg):
        self.pos = pos
        self.v = v
        self.dmg = dmg
