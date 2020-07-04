import pygame
from random import randint

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
        self.exploded_color_1 = [randint(180,255),randint(180,255),randint(180,255)]
        self.exploded_color_2 = self.exploded_color_1
        self.exploded_1_radius = -31
        self.exploded_2_radius = self.x_offset
        self.exploded_1_width = 10
        self.exploded_2_width = 5

    def draw(self, display):
        display.blit(self.sprite, (self.x,self.y))

    def explode_1(self, display):
        if self.exploded_1_radius < 31:
            pygame.draw.circle(display, self.exploded_color_1, (round(self.x+self.x_offset), round(self.y+self.y_offset)), 10+round(-(0.1*self.exploded_1_radius)**2+10)*3, self.exploded_1_width)
            self.exploded_1_radius += 1
            self.exploded_color_1 = [x+1 if x < 255 else x for x in self.exploded_color_1 ]

    def explode_2(self, display):
        self.exploded_2_radius += 5
        pygame.draw.circle(display, self.exploded_color_2, (round(self.x+self.x_offset), round(self.y+self.y_offset)), self.exploded_2_radius, self.exploded_2_width)
        self.exploded_color_2 = [x-2 if x > 2 else x for x in self.exploded_color_2 ]
