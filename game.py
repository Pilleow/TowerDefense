from enemies import *
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

class Game:
    def __init__(self):
        self.resolution = (1200,720)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.projectiles = []
        self.enemies = [Circle_1()]
        self.turrets = []
        self.health = 50
        self.money = 250

    def draw(self):
        for en in self.enemies:
            en.draw()
        for tr in self.turrets:
            tr.draw()
        for pr in self.projectiles:
            pr.draw()

    def run(self):
        run = True
        FPS = 60

        while run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

g = Game()
g.run()

pygame.quit()
