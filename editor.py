from obj.button import Button
import pygame
import math
import json

text_font = pygame.font.SysFont('Consolas', 50)

class Editor():
    def __init__(self):
        self.resolution = (1200,720)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.buttons = [Button([50,200,50], (self.resolution[0]//1.3, self.resolution[1]//1.2, 200, 50), "Save", [0,0,0], 30)] # color, pos_res, text, text_color, font, antialias=True
        self.path_saved_text = text_font.render("Level saved to data/levels.json", True, (255,255,255))
        self.path_saved_text_center = self.path_saved_text.get_rect(center=(self.resolution[0]//2, self.resolution[1]//15))
        self.path_saved_text_timeout = 0
        self.path = []
        self.path_saved = False

    def run(self):
        run = True
        FPS = 60
        while run:
            self.clock.tick(FPS)

            if self.path_saved_text_timeout == 0:
                self.path_saved = False
                self.path_saved_text_timeout -= 1

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN: # left click = 1; right click = 3
                    if self.buttons[0].isOver(pos):
                        self.savePath()
                    else:
                        self.modifyPath(pos)

                if event.type == pygame.MOUSEMOTION:
                    if self.buttons[0].isOver(pos):
                        self.buttons[0].color = self.buttons[0].clicked_color
                    else:
                        self.buttons[0].color = self.buttons[0].default_color
            self.draw()

    def modifyPath(self, pos):
        path_pos = (math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50)
        if path_pos not in self.path:
            self.path.append(path_pos)
        elif path_pos in self.path:
            for p in self.path:
                if path_pos == p:
                    self.path.remove(p)

    def draw(self):
        self.Screen.fill((0,0,0))

        for p in self.path:
            if self.path.index(p) == 0:
                pygame.draw.rect(self.Screen, (100,200,100), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (150,250,150), (p[0]+5, p[1]+5, 40, 40))
            else:
                pygame.draw.rect(self.Screen, (100,100,100), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (150,150,150), (p[0]+5, p[1]+5, 40, 40))

        for b in self.buttons:
            b.draw(self.Screen)

        if self.path_saved == True:
            self.Screen.blit(self.path_saved_text, self.path_saved_text_center)
            self.path_saved_text_timeout -= 1

        pygame.display.update()

    def savePath(self):
        with open("data/levels.json") as f:
            levels = json.load(f)

        levels.append(self.path)
        self.path_saved = True
        self.path_saved_text_timeout = 300
        self.path = []

        with open("data/levels.json", "w") as f:
            json.dump(levels, f)

e = Editor()
e.run()

pygame.quit()
