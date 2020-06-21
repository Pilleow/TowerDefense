import pygame


class Enemy:
    def __init__(self, pos, v, health, dmg, sprite):
        self.pos = pos
        self.v = v
        self.health = health
        self.dmg = dmg
        self.sprite = sprite

    def checkCollision(self):
        pass

    def draw(self, display):
        display.blit(self.sprite, self.pos)

