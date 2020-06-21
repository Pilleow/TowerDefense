import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()


class Enemy:
    def __init__(self, pos, v, health, dmg, sprite):
        self.x_offset = sprite.get_rect().size[0]//2
        self.y_offset = sprite.get_rect().size[1]//2
        self.x = pos[0]+25-self.x_offset
        self.y = pos[1]+25-self.y_offset
        self.v = v
        self.health = health
        self.dmg = dmg
        self.sprite = sprite
        self.point = 0

    def checkCollision(self):
        pass

    def draw(self, display):
        display.blit(self.sprite, (self.x,self.y))

