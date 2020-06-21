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
        self.wave = 0
        self.enemy_send_timer = 100
        self.enemy_send_index = 0
        self.enemy_type_index = 0

        with open("data/levels.json") as f:
            self.levels = json.load(f)
        with open("data/waves.json") as f:
            self.waves = json.load(f)

    def draw(self):
        self.Screen.fill((0,0,0))

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

        for en in self.enemies:
            en.draw(self.Screen)
        for tr in self.turrets:
            tr.draw(self.Screen)
        for pr in self.projectiles:
            pr.draw(self.Screen)

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

            # sending enemies
            if self.enemy_send_timer > 0:
                self.enemy_send_timer -= 1
            else:
                self.enemies.append(eval(f"{self.waves[self.wave][self.enemy_type_index][0]}(self.levels[self.level][0])"))
                self.enemy_send_index += 1
                self.enemy_send_timer = 40

                if self.enemy_send_index >= self.waves[self.wave][self.enemy_type_index][1]:
                    if len(self.waves[self.wave])-1 <= self.enemy_type_index:

                        if self.wave != len(self.waves)-1:
                            self.wave += 1
                            self.enemy_send_timer = 300
                            self.enemy_send_index = 0
                            self.enemy_type_index = 0
                        else:
                            print('Game Finished - No more waves left')

                    else:
                        self.enemy_send_index = 0
                        self.enemy_type_index += 1

            # moving enemies, checking if any came to the end
            for en in self.enemies:
                x_value = en.x-25+en.x_offset
                y_value = en.y-25+en.y_offset
                x_distance = abs(x_value - self.levels[self.level][en.point][0])
                y_distance = abs(y_value - self.levels[self.level][en.point][1])

                if x_value > self.levels[self.level][en.point][0]:
                    if x_distance >= en.v:
                        en.x -= en.v
                    else:
                        en.x -= x_distance - en.v
                elif x_value < self.levels[self.level][en.point][0]:
                    if x_distance >= en.v:
                        en.x += en.v
                    else:
                        en.x += x_distance - en.v
                elif y_value > self.levels[self.level][en.point][1]:
                    if y_distance >= en.v:
                        en.y -= en.v
                    else:
                        en.y -= y_distance - en.v
                elif y_value < self.levels[self.level][en.point][1]:
                    if y_distance >= en.v:
                        en.y += en.v
                    else:
                        en.y += y_distance - en.v

                else:
                    if en.point >= len(self.levels[self.level])-1:
                        self.health -= en.dmg
                        self.enemies.remove(en)
                        print(self.health)
                    else:
                        en.point += 1

            self.draw()

    def loadLevel(self):
        for square in self.levels[self.level]:
            for offset in [[0,50],[50,50],[50,0],[50,-50],[0,-50],[-50,-50],[-50,0],[-50,50]]:

                if not [square[0]+offset[0], square[1]+offset[1]] in self.levels[self.level]:
                    self.tiles.append([square[0]+offset[0], square[1]+offset[1]])


g = Game()
g.run()

pygame.quit()

