import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()


class Tower:
    def __init__(self, pos, dmg, cost, sprite):
        self.pos = pos
        self.dmg = dmg
        self.cost = cost
        self.sprite = sprite # list containing base and head of a turret

    def draw(self, display):
        for s in self.sprite:
            display.blit(s, self.pos)
