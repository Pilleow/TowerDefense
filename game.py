from objects import *
import pygame
import json
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

text_font_m = pygame.font.SysFont('Consolas', 50)
text_font_s = pygame.font.SysFont('Consolas', 30)


class Game:
    def __init__(self):
        self.resolution = (1000,700)
        self.Screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.tiles = []
        self.projectiles = []
        self.enemies = []
        self.turrets = []
        self.turret_pos = []
        self.available_turrets = [eval(f"Kinetic_{x}([-1000, -1000], False)") for x in range(1,4)]
        self.health = 500
        self.money = 250
        self.level = 0
        self.wave = 0
        self.enemy_send_timer = 300
        self.enemy_send_index = 0
        self.enemy_type_index = 0
        self.buy_menu_open = False
        self.buy_menu_width = len(self.available_turrets)
        self.buy_menu_pos = [-50,-100]

        with open("data/levels.json") as f:
            self.levels = json.load(f)
        with open("data/waves.json") as f:
            self.waves = json.load(f)

        self.turret_cost_text = text_font_m.render("", True, (255,255,255))
        self.turret_cost_center = self.turret_cost_text.get_rect(center=(self.resolution[0]//2, 60))
        self.notif_text = text_font_s.render("", True, (255,100,100))
        self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 105))
        self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
        self.health_text = text_font_m.render(str(self.health), True, (255,150,150))

    def run(self):
        """
        Main loop, runs every frame
        :returns: None
        """
        run = True
        FPS = 60
        self.loadLevel()

        while run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    run = False

                if event.type == pygame.MOUSEMOTION:

                    pos = pygame.mouse.get_pos()
                    hovered_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))

                    if self.buy_menu_open:
                        for tr in self.available_turrets:
                            if hovered_tile != tr.pos:
                                continue

                            self.turret_cost_text = text_font_m.render(str(tr.cost)+" $", True, (255,255,255))
                            self.turret_cost_center = self.turret_cost_text.get_rect(center=(self.resolution[0]//2, 60))
                            self.notif_text = text_font_s.render("", True, (255,100,100))
                            if self.money >= tr.cost:
                                continue

                            self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
                            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 105))
                            break

                if event.type == pygame.MOUSEBUTTONDOWN: # activating buy/turret menu

                    selected_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))
                    if selected_tile in self.turret_pos and not self.buy_menu_open:
                        print('Open Tower Modification Menu (WIP)')

                    elif self.buy_menu_open:
                        if (selected_tile[0] < self.buy_menu_pos[0] or selected_tile[0] > self.buy_menu_pos[0] + 50*(self.buy_menu_width-1)) or (selected_tile[1] < self.buy_menu_pos[1] or selected_tile[1] > self.buy_menu_pos[1]):
                            self.turret_cost_text = text_font_m.render("", True, (255,255,255))
                            self.notif_text = text_font_s.render("", True, (255,100,100))
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
                                    self.turret_cost_text = text_font_m.render("", True, (255,255,255))
                                break

                    elif selected_tile in self.tiles:
                        self.buy_menu_open = True
                        self.buy_menu_pos = [selected_tile[0] + 50, selected_tile[1]]
                        count = 0
                        for tr in self.available_turrets:
                            tr.__init__([self.buy_menu_pos[0] + 50 * count, self.buy_menu_pos[1]], False)
                            count += 1

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
                            run = False

            self.detectEnemy()
            self.draw()

    def loadLevel(self):
        """
        Loads level from levels.json, autofills the surrounding area around path
        :returns: None
        """
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
                    if en.health <= 0:
                        self.money += en.value
                        self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))
                        self.enemies.remove(en)

    def draw(self):
        """
        Draws all of the elements on the display, updates the display
        :returns: None
        """
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

        # GUI here
        if self.buy_menu_open:
            pygame.draw.rect(self.Screen, [100,100,100], (self.buy_menu_pos[0], self.buy_menu_pos[1], 50*self.buy_menu_width, 50))
            pygame.draw.rect(self.Screen, [80,80,80], (self.buy_menu_pos[0]+5, self.buy_menu_pos[1]+5, 50*self.buy_menu_width-10, 40))
            for tr in self.available_turrets:
                tr.draw(self.Screen)
            Screen.blit(self.turret_cost_text, self.turret_cost_center)

        Screen.blit(self.notif_text, self.notif_text_center)
        Screen.blit(self.money_text, (26,26))
        Screen.blit(self.health_text, (26,76))

        pygame.display.update()


g = Game()
g.run()

pygame.quit()

