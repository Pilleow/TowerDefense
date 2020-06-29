from obj.button import Button
import pygame
import math
import json

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

text_font = pygame.font.SysFont('Consolas', 50)

class Editor():
    def __init__(self):
        self.resolution = (1000,700)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.buttons = [Button([50,200,50], (self.resolution[0]//1.4, self.resolution[1]//1.2, 200, 60), "Save", [0,0,0], 40)] # color, pos_res, text, text_color, font, antialias=True
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
                self.path = []
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
        path_pos = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))
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
                pygame.draw.rect(self.Screen, (200,100,100), (p[0], p[1], 50, 50))
                pygame.draw.rect(self.Screen, (250,150,150), (p[0]+5, p[1]+5, 40, 40))
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
        # centering the path
        
        x_min = self.path[0][0]
        x_max = x_min
        y_min = self.path[0][1]
        y_max = y_min

        for square in self.path:
            if square[0] < x_min:
                x_min = square[0]
            elif square[0] > x_max:
                x_max = square[0]

            if square[1] < y_min:
                y_min = square[1]
            elif square[1] > y_max:
                y_max = square[1]

        x_center = (x_max+x_min)//2
        y_center = (y_max+y_min)//2
        x_offset = self.resolution[0]//2 - x_center
        y_offset = self.resolution[1]//2 - y_center

        if x_offset % 2:
            x_offset -= 25
        if y_offset % 2:
            y_offset += 25

        for square in self.path:
            square[0] += x_offset
            square[1] += y_offset

        print(x_offset)
        print(y_offset)

        # saving path
        with open("data/levels.json") as f:
            levels = json.load(f)

        levels.append(self.path)
        self.path_saved = True
        self.path_saved_text_timeout = 300
        #self.path = []

        with open("data/levels.json", "w") as f:
            json.dump(levels, f)

e = Editor()
e.run()

pygame.quit()
