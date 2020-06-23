import pygame


class Enemy:
    def __init__(self, pos, v, health, dmg, value, sprite):
        self.x_offset = sprite.get_rect().size[0]//2
        self.y_offset = sprite.get_rect().size[1]//2
        self.x = pos[0]+25-self.x_offset
        self.y = pos[1]+25-self.y_offset
        self.v = 50/v
        self.health = health
        self.dmg = dmg
        self.sprite = sprite
        self.value = value
        self.point = 0

    def draw(self, display):
        display.blit(self.sprite, (self.x,self.y))

