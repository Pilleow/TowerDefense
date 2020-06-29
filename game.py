from objects import *
from random import choice
import pygame
import json
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

text_font_l = pygame.font.SysFont('Consolas', 100)
text_font_m = pygame.font.SysFont('Consolas', 50)
text_font_s = pygame.font.SysFont('Consolas', 30)


class Game:
    def __init__(self):
        self.resolution = (1000,700)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("sprites/other/background.png").convert()
        self.backgrounds = [[self.bg, [self.resolution[0]*x, 0]] for x in range(3)]
        self.tiles = []
        self.enemies = []
        self.turrets = []
        self.turret_pos = []
        self.available_turrets = [eval(f"Kinetic_{x}([-1000, -1000], False)") for x in range(1,4)]
        self.turret_menu_buttons = [ [x, [-50,-100], pygame.transform.scale(pygame.image.load(f"sprites/buttons/turretMenu/{x}.png"),(40,40))] for x in ['sell','upgrade'] ]
        self.buy_menu_pos = [-50,-100]
        self.turret_menu_pos = [-50,-100]
        self.buy_menu_width = len(self.available_turrets)
        self.turret_menu_width = len(self.turret_menu_buttons)
        self.health = 50
        self.money = 300
        self.level = -1
        self.wave = 0
        self.FPS = 60
        self.enemy_send_timer = 300
        self.enemy_send_index = 0
        self.enemy_type_index = 0
        self.run = True
        self.buy_menu_open = False
        self.turret_menu_open = False

        with open("data/levels.json") as f:
            self.levels = json.load(f)
        with open("data/waves.json") as f:
            self.waves = json.load(f)

        self.title_text = text_font_l.render("Tower Defence", True, (250,250,250))
        self.title_text_center = self.title_text.get_rect(center=(self.resolution[0]//2, self.resolution[1]//5))
        self.turret_cost_text = text_font_m.render(" ", True, (255,255,255))
        self.turret_cost_center = self.turret_cost_text.get_rect(center=(self.resolution[0]//2, 30))
        self.notif_text = text_font_s.render(" ", True, (255,100,100))
        self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 70))
        self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
        self.health_text = text_font_m.render(str(self.health), True, (255,150,150))

        self.new_game_button = newGame((self.resolution[0]//3.5-175, self.resolution[1]//2, 350, 80))

    def mainMenu(self):
        """
        Main loop, runs on game launch
        :returns: None
        """
        self.loadLevel()
        self.enemy_send_timer = 60

        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()

                    if self.new_game_button.isOver(pos):
                        self.new_game_button.color =self.new_game_button.clicked_color
                    else:
                        self.new_game_button.color = self.new_game_button.default_color

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.new_game_button.isOver(pos):
                        self.gameRun()

            if self.enemy_send_timer > 0:
                self.enemy_send_timer -= 1
            else:
                self.enemies.append(eval(f'{choice(["Circle_1", "Circle_2","Square_1","Square_2"])}(self.levels[self.level][0])'))
                self.enemy_send_timer = 60
                self.health = 50

            for en in self.enemies:
                self.moveEnemy(en)

            self.drawMenu()

    def gameRun(self):
        """
        Main loop, runs when a level is being played
        :returns: None
        """
        self.loadLevel()

        while self.run: # mainloop ---------------------------------------------------------------- #
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.run = False

                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()
                    hovered_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))

                    if self.buy_menu_open:
                        for tr in self.available_turrets:
                            if hovered_tile != tr.pos:
                                continue

                            self.turret_cost_text = text_font_m.render(str(tr.cost)+" $", True, (255,255,255))
                            self.turret_cost_center = self.turret_cost_text.get_rect(center=(self.resolution[0]//2, 30))
                            self.notif_text = text_font_s.render(" ", True, (255,100,100))
                            if self.money >= tr.cost:
                                continue

                            self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
                            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 70))
                            break

                if event.type == pygame.MOUSEBUTTONDOWN:

                    selected_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))
    
                    # buy menu is active -------------------------------------------------------- #
                    if self.buy_menu_open:
                        if selected_tile[0] < self.buy_menu_pos[0] or selected_tile[0] > self.buy_menu_pos[0] + 50*(self.buy_menu_width-1) or selected_tile[1] < self.buy_menu_pos[1] or selected_tile[1] > self.buy_menu_pos[1]:
                            self.turret_cost_text = text_font_m.render(" ", True, (255,255,255))
                            self.notif_text = text_font_s.render(" ", True, (255,100,100))
                            self.buy_menu_open = False

                        else:
                            for tr in self.available_turrets:
                                if tr.pos != selected_tile:
                                    continue

                                if self.money >= tr.cost:
                                    pos = [self.buy_menu_pos[0]-50, self.buy_menu_pos[1]]
                                    self.turrets.append(eval(f"{tr.__class__.__name__}({pos}, True)"))
                                    self.turret_pos.append(pos)
                                    self.buy_menu_open = False
                                    self.money -= tr.cost
                                    self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
                                    self.turret_cost_text = text_font_m.render(" ", True, (255,255,255))
                                    self.notif_text = text_font_s.render(" ", True, (255,100,100))
                                break

                    # turret menu is active -------------------------------------------------------- #
                    elif self.turret_menu_open:
                        if selected_tile[0] < self.turret_menu_pos[0] or selected_tile[0] > self.turret_menu_pos[0]+50*(self.turret_menu_width-1) or selected_tile[1] < self.turret_menu_pos[1] or selected_tile[1] > self.turret_menu_pos[1]:
                            self.turret_menu_open = False
                            self.selected_turret.show_range = False

                        else:
                            for btn in self.turret_menu_buttons:
                                if [btn[1][0]-5, btn[1][1]-5] != selected_tile: # btn[2] = sprite; btn[1] = position; btn[0] = type
                                    continue
                                    
                                if btn[0] == 'sell':
                                    self.money += round(self.selected_turret.cost*0.8)
                                    self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
                                    self.turrets.remove(self.selected_turret)
                                    self.turret_pos.remove(self.selected_turret.pos)
                                    self.selected_turret.show_range = False
                                    self.turret_menu_open = False

                                elif btn[0] == 'upgrade':
                                    if self.money >= tr.cost*0.5:
                                        prev_cost = tr.cost
                                        if tr.upgrade():
                                            self.money -= round(prev_cost*0.5)
                                            self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
                                    else:
                                        print('not enough money')

                                break

                    # opening turret menu ----------------------------------------------------- #
                    elif selected_tile in self.turret_pos:
                        self.turret_menu_open = True
                        self.turret_menu_pos = [selected_tile[0] + 50, selected_tile[1]]

                        count = 0
                        for btn in self.turret_menu_buttons:
                            btn[1][0] = self.turret_menu_pos[0] + 50 * count + 5
                            btn[1][1] = self.turret_menu_pos[1] + 5
                            count += 1

                        for tr in self.turrets:
                            if tr.pos != selected_tile:
                                continue

                            self.selected_turret = tr
                            self.selected_turret.show_range = True
                            break

                    # opening buy menu -------------------------------------------------------- #
                    elif selected_tile in self.tiles:
                        self.buy_menu_open = True
                        self.buy_menu_pos = [selected_tile[0] + 50, selected_tile[1]]

                        count = 0
                        for tr in self.available_turrets:
                            tr.__init__([self.buy_menu_pos[0] + 50 * count, self.buy_menu_pos[1]], False)
                            count += 1

            # sending enemies -------------------------------------------------------- #
            if self.enemy_send_timer > 0:
                self.enemy_send_timer -= 1
            else:
                self.enemies.append(eval(f"{self.waves[self.wave][self.enemy_type_index][0]}(self.levels[self.level][0])"))
                self.enemy_send_index += 1
                self.enemy_send_timer = self.waves[self.wave][self.enemy_type_index][2]

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

            # moving enemies, checking if any came to the end -------------------- #
            for en in self.enemies:
                self.moveEnemy(en)

            self.detectEnemy()
            self.drawGame()

    def loadLevel(self):
        """
        Loads level from levels.json, autofills the surrounding area around path
        :returns: None
        """
        self.health = 50
        self.money = 300
        self.wave = 0
        self.enemy_send_timer = 300
        self.enemy_send_index = 0
        self.enemy_type_index = 0
        self.level += 1
        self.enemies = []
        self.tiles = []
        self.turrets = []

        self.level_length = len(self.levels[self.level])
        for square in self.levels[self.level]:
            for offset in [[0,50],[50,50],[50,0],[50,-50],[0,-50],[-50,-50],[-50,0],[-50,50]]:

                if not [square[0]+offset[0], square[1]+offset[1]] in self.levels[self.level]:
                    self.tiles.append([square[0]+offset[0], square[1]+offset[1]])

    def detectEnemy(self):
        """
        Detects if an enemy is in range of a turret
        :returns: None
        """
        for tr in self.turrets:
            if tr.shoot_cooldown > 0:
                tr.shoot_cooldown -= 1
            for en in self.enemies:
                distance = math.hypot(tr.x - en.x, tr.y - en.y)
                if distance <= tr.range_ and tr.shoot_cooldown <= 0:
                    tr.shoot_cooldown = tr.shoot_cooldown_default
                    en.health -= tr.dmg
                    tr.target = (en.x+en.x_offset, en.y+en.y_offset)
                    tr.beam_drawtime = 7
                    if en.health <= 0:
                        self.money += en.value
                        self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
                        self.enemies.remove(en)
                    break

    def moveEnemy(self,en):
        """
        Moves an enemy to the next path point by its self.v value
        :returns: None
        """
        x_value = en.x-25+en.x_offset
        y_value = en.y-25+en.y_offset

        if x_value > self.levels[self.level][en.point][0]:
            en.x -= en.v
        elif x_value < self.levels[self.level][en.point][0]:
            en.x += en.v
        elif y_value > self.levels[self.level][en.point][1]:
            en.y -= en.v
        elif y_value < self.levels[self.level][en.point][1]:
            en.y += en.v

        else:
            if en.point+1 < self.level_length:
                en.point += 1
            else:
                self.health -= en.dmg
                self.enemies.remove(en)
                self.health_text = text_font_m.render(str(self.health), True, (255,150,150))
                if self.health <= 0:
                    print("Game Over - No lives left.")
                    self.run = False

    def drawBg(self):
        """
        Draws the background image sliding to the left
        :returns: None
        """

        for bg in self.backgrounds:
            self.Screen.blit(bg[0],bg[1])
            bg[1][0] -= 1
            if bg[1][0] < -self.resolution[0]:
                self.backgrounds.append([self.bg, [self.resolution[0]*2, 0]])
                self.backgrounds.remove(bg)

    def drawMenu(self):
        self.drawBg()

        Screen.blit(self.title_text, self.title_text_center)
        self.new_game_button.draw(self.Screen)

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

        pygame.display.update()

    def drawGame(self):
        """
        Draws all of the level elements except the background on the display, updates the display
        :returns: None
        """
        self.drawBg()

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

        # GUI
        if self.buy_menu_open:
            pygame.draw.rect(self.Screen, [100,100,100], (self.buy_menu_pos[0], self.buy_menu_pos[1], 50*self.buy_menu_width, 50))
            pygame.draw.rect(self.Screen, [80,80,80], (self.buy_menu_pos[0]+5, self.buy_menu_pos[1]+5, 50*self.buy_menu_width-10, 40))
            pygame.draw.rect(self.Screen, [100,100,100], (self.resolution[0]//2 - 220, 0, 440, 120))
            pygame.draw.rect(self.Screen, [80,80,80], (self.resolution[0]//2 - 200, 0, 400, 100))

            for tr in self.available_turrets:
                tr.draw(self.Screen)

            Screen.blit(self.turret_cost_text, self.turret_cost_center)
            Screen.blit(self.notif_text, self.notif_text_center)

        elif self.turret_menu_open:
            pygame.draw.rect(self.Screen, [100,100,100], (self.turret_menu_pos[0], self.turret_menu_pos[1], 50*self.turret_menu_width, 50))
            pygame.draw.rect(self.Screen, [80,80,80], (self.turret_menu_pos[0]+5, self.turret_menu_pos[1]+5, 50*self.turret_menu_width-10, 40))

            for btn in self.turret_menu_buttons:
                self.Screen.blit(btn[2],btn[1])

        Screen.blit(self.money_text, (26,26))
        Screen.blit(self.health_text, (26,76))

        pygame.display.update()


g = Game()
g.mainMenu()

pygame.quit()

