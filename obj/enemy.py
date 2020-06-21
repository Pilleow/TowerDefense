import pygame

class Enemy:
    def __init__(self, v, health, dmg):
        self.pos = ()
        self.v = v
        self.health = health
        self.dmg = dmg

    def checkCollision(self):
        pass

    def draw(self):
        pass

