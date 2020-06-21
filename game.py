from objects import *
import pygame
import json

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

class Game:
    def __init__(self):
        self.resolution = (1000,700)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.tiles = []
        self.projectiles = []
        self.enemies = []
        self.turrets = []
        self.health = 50
        self.money = 250
        self.level = 0

        with open("data/levels.json") as f:
            self.levels = json.load(f)

    def draw(self):
        self.Screen.fill((0,0,0))
        for en in self.enemies:
            en.draw()
        for tr in self.turrets:
            tr.draw()
        for pr in self.projectiles:
            pr.draw()
        for p in self.levels[self.level]:
            if self.levels[self.level].index(p) == 0:
                pygame.draw.rect(self.Screen, (200,100,100), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (250,150,150), (p[0]+5, p[1]+5, 40, 40))
            elif self.levels[self.level].index(p) == len(self.levels[self.level])-1:
                pygame.draw.rect(self.Screen, (100,200,100), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (150,250,150), (p[0]+5, p[1]+5, 40, 40))
            else:
                pygame.draw.rect(self.Screen, (140,140,140), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (170,170,170), (p[0]+5, p[1]+5, 40, 40))

        for t in self.tiles:
            pygame.draw.rect(self.Screen, (40,40,40), (t[0], t[1], 50, 50))
            pygame.draw.rect(self.Screen, (70,70,70), (t[0]+5, t[1]+5, 40, 40))

        pygame.display.update()

    def run(self):
        run = True
        FPS = 60
        self.loadLevel()

        while run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.draw()

    def loadLevel(self):
        for square in self.levels[self.level]:
            for offset in [[0,50],[50,50],[50,0],[50,-50],[0,-50],[-50,-50],[-50,0],[-50,50]]:
                print("executed")
                if not [square[0]+offset[0], square[1]+offset[1]] in self.levels[self.level]:
                    self.tiles.append([square[0]+offset[0], square[1]+offset[1]])


g = Game()
g.run()

pygame.quit()
