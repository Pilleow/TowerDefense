import objects.objects as objects
from objects.menu import buyMenu, turretMenu, settingsMenu
from random import choice, randint
import json, math
import pygame

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.display.set_icon(pygame.image.load("sprites/other/icon.gif"))
pygame.display.set_caption("Tower Defence by Pilleow")

text_font_xl = pygame.font.Font('media/other/Adobe Dia.ttf', 200)
text_font_l = pygame.font.Font('media/other/Adobe Dia.ttf', 90)
text_font_m = pygame.font.Font('media/other/Adobe Dia.ttf', 70)
text_font_s = pygame.font.Font('media/other/Adobe Dia.ttf', 50)

class Game:
    def __init__(self):
        self.resolution = (1000,700)
        self.clock = pygame.time.Clock()
        self.Screen = pygame.display.set_mode(self.resolution)

        self.indicator = pygame.image.load('sprites/other/indicator.png').convert_alpha()

        self.tiles = []
        self.killed_enemies = []
        self.enemies = []
        self.turrets = []
        self.turret_pos = []
        self.parallax_move = [0,0]
        self.buy_menu_pos = [-50,-100]
        self.turret_menu_pos = [-50,-100]
        self.hue = choice([[255,0,0],[0,255,0],[0,0,255]])
        self.hovered_tile = self.resolution
        self.intro_sfx = [pygame.mixer.Sound(f"media/intro/sfx_{index}.wav") for index in range(1,4)]
        self.available_turrets = [eval(f"objects.Kinetic_{x}([-1000, -1000], False)") for x in range(1,4)]
        self.tile_sprites = [pygame.image.load(f'sprites/path/tile_{x}.png').convert() for x in range(1,5)]
        self.intro_frames = [pygame.image.load(f"media/intro/frame_{index}.png").convert() for index in range(1,10)]
        self.backgrounds = [[pygame.image.load("sprites/other/background.png").convert(), [self.resolution[0]*x, -50]] for x in range(-1,2)]
        self.turret_menu_buttons = [ [x, [-50,-100], pygame.transform.scale(pygame.image.load(f"sprites/buttons/turretMenu/{x}.png"),(40,40))] for x in ['sell','upgrade'] ]

        self.sfx = {
            "menu_nav": pygame.mixer.Sound("media/sfx/menu_nav.wav")
        }

        self.FPS = 90
        self.NOTIF_Y = 100
        self.COST_Y = 50

        self.turret_menu_width = len(self.turret_menu_buttons)
        self.buy_menu_width = len(self.available_turrets)
        self.enemy_send_timer = 300
        self.enemy_send_index = 0
        self.enemy_type_index = 0
        self.intro_frame_count = 0
        self.intro_timer = 30
        self.health = 50
        self.money = 500
        self.level = -1
        self.wave = 0
        self.kills = 0

        self.turret_menu_open = False
        self.buy_menu_open = False
        self.intro_playing = True
        self.intro_menu_t_played = False
        self.run = True

        self.title_text = text_font_xl.render("Tower Defence", True, (250,250,250))
        self.cost_text = text_font_m.render(" ", True, (255,255,255))
        self.notif_text = text_font_s.render(" ", True, (255,100,100))
        self.money_text = text_font_l.render(str(self.money)+" $", True, (255,255,255))
        self.health_text = text_font_l.render(str(self.health), True, (255,150,150))
        self.music_credits_text = text_font_m.render("Music - Adam Haynes", True, (150,255,150))
        self.art_credits_text = text_font_m.render("Art - Kenney Vleugels & Igor Zamojski", True, (150,255,150))
        self.dev_credits_text = text_font_m.render("Development - Igor Zamojski", True, (150,255,150))
        self.game_over_text_1 = text_font_xl.render("Game Over", True, (255,255,255))
        self.game_over_text_2 = text_font_l.render("Good luck next time!", True, (155,155,155))
        self.game_over_stats = text_font_m.render(f"Kills: {self.kills}", True, (200,200,200))

        self.title_text_center = self.title_text.get_rect(center=(self.resolution[0]//2, self.resolution[1]//5))
        self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0], self.COST_Y+self.parallax_move[1]))
        self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0], self.NOTIF_Y+self.parallax_move[1]))
        self.music_credits_text_center = self.music_credits_text.get_rect(center=(self.resolution[0]/2, self.resolution[1]/2+100))
        self.art_credits_text_center = self.art_credits_text.get_rect(center=(self.resolution[0]/2, self.resolution[1]/2))
        self.dev_credits_text_center = self.dev_credits_text.get_rect(center=(self.resolution[0]/2, self.resolution[1]/2-100))
        self.game_over_text_1_center = self.game_over_text_1.get_rect(center=(self.resolution[0]//2, self.resolution[1]//4-5))
        self.game_over_text_2_center = self.game_over_text_2.get_rect(center=(self.resolution[0]//2, self.resolution[1]//4+75))
        self.game_over_stats_center = self.game_over_stats.get_rect(center=(self.resolution[0]//2, self.resolution[1]//2))

        self.new_game_button = objects.newGameButton((self.resolution[0]/3.5-175, 255, 350, 80))
        self.settings_button = objects.settingsButton((self.resolution[0]/3.5-175, 385, 350, 80))
        self.credits_button = objects.creditsButton((self.resolution[0]/3.5-175, 515, 350, 80))
        self.main_menu_buttons = [self.new_game_button, self.settings_button, self.credits_button]
        self.audio_settings_button = objects.audioSettingsButton((self.resolution[0]/2-260, self.resolution[1]/2-120, 520, 100))
        self.video_settings_button = objects.videoSettingsButton((self.resolution[0]/2-260, self.resolution[1]/2+35, 520, 100))
        self.back_settings_button = objects.backSettingsButton((self.resolution[0]/2-75, self.resolution[1]/1.275, 150, 80))
        self.settings_buttons = [self.audio_settings_button, self.video_settings_button, self.back_settings_button]
        self.try_again_button = objects.tryAgainButton((self.resolution[0]/2-260, self.resolution[1]/2+75, 520, 100))

        with open("data/levels.json") as f:
            self.levels = json.load(f)
        with open("data/waves.json") as f:
            self.waves = json.load(f)
        with open("data/settings.json") as f:
            settings = json.load(f)
            self.music_volume = settings['music_volume']
            self.sfx_volume = settings['sfx_volume']
            self.parallax_mod = settings['parallax_mod']

        for key in self.sfx:
            self.sfx[key].set_volume(self.sfx_volume)

    def playIntro(self):
        """
        Main loop, runs on game launch - shows intro, non-interactable
        :returns: None
        """
        while self.intro_playing:
            self.clock.tick(self.FPS)

            # exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.intro_playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.intro_playing = False

            # timer / countdown
            if self.intro_timer > 0:
                self.intro_timer -= 1
                continue

            # playing sfx
            if self.intro_frame_count == 0:
                self.intro_sfx[0].play()
            elif self.intro_frame_count == 7:
                self.intro_sfx[1].play()
            elif self.intro_frame_count == 8:
                self.intro_sfx[2].play()

            # drawing
            if self.intro_frame_count < 9:
                self.Screen.blit(self.intro_frames[self.intro_frame_count], [0,0])
                self.intro_frame_count += 1
            else:
                self.Screen.fill((0,0,0))
                self.intro_frame_count += 1

            # setting new timer / countdown
            if self.intro_frame_count < 7:
                self.intro_timer = 6
            elif self.intro_frame_count == 7:
                self.intro_timer = 24
            elif self.intro_frame_count == 8:
                self.intro_timer = 90
            elif self.intro_frame_count == 9:
                self.intro_timer = 18
            elif self.intro_frame_count == 10:
                self.intro_timer = 80
            elif self.intro_frame_count == 11:
                self.intro_playing = False

            pygame.display.update()

        if self.run:
            self.mainMenu()

    def mainMenu(self):
        """
        Main loop, runs after self.playIntro()
        :returns: None
        """
        self.loadMusic("main_menu.mp3", self.music_volume)
        self.loadLevel()
        self.enemy_send_timer = 60

        while self.run: # mainloop ---------------------------------------------------------------- #
            self.clock.tick(self.FPS)
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEMOTION:

                    self.setParallax()
                    for button in self.main_menu_buttons:
                        if button.isOver(pos):
                            button.color = button.clicked_color
                        else:
                            button.color = button.default_color

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()

                    if self.main_menu_buttons[0].isOver(pos): # new game
                        self.main_menu_buttons[0].color = self.main_menu_buttons[0].default_color
                        self.sfx['menu_nav'].play()
                        self.loadMusic("level.mp3", self.music_volume)
                        self.gameRun()

                    elif self.main_menu_buttons[1].isOver(pos): # settings
                        self.main_menu_buttons[1].color = self.main_menu_buttons[1].default_color
                        self.sfx['menu_nav'].play()
                        settingsMenu.settings_active(self)

                    elif self.main_menu_buttons[2].isOver(pos): # credits
                        self.main_menu_buttons[2].color = self.main_menu_buttons[2].default_color
                        self.sfx['menu_nav'].play()
                        self.showCredits()

            if self.enemy_send_timer > 0:
                self.enemy_send_timer -= 1
            else:
                self.enemies.append(eval(f'objects.{choice(["Circle_1", "Circle_2","Square_1","Square_2"])}(self.levels[self.level][0])'))
                self.enemy_send_timer = 60
                self.health = 50

            for en in self.enemies:
                self.moveEnemy(en)

            if self.run:
                self.drawMenu()

    def gameOver(self):
        """
        Main loop, runs when credits are selected in mainMenu
        :returns: None
        """
        self.game_over_stats = text_font_m.render(f"Kills: {self.kills}", True, (200,200,200))
        self.level = -1
        pygame.mixer.music.stop()
        show_game_over = True
        while show_game_over and self.run: # mainloop ---------------------------------------------------------------- #
            self.clock.tick(self.FPS)
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEMOTION:
                    self.setParallax()

                    if self.try_again_button.isOver(pos):
                        self.try_again_button.color = self.try_again_button.clicked_color
                    else:
                        self.try_again_button.color = self.try_again_button.default_color

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.try_again_button.isOver(pos):
                        self.sfx['menu_nav'].play()
                        show_game_over = False

            self.drawGameOver()

        self.loadLevel()

    def showCredits(self):
        """
        Main loop, runs when credits are selected in mainMenu
        :returns: None
        """
        show_credits = True
        while show_credits: # mainloop ---------------------------------------------------------------- #
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_credits = False

                if event.type == pygame.MOUSEMOTION:
                    self.setParallax()

            self.drawCredits()

    def gameRun(self):
        """
        Main loop, runs when a level is being played
        :returns: None
        """
        self.loadLevel()
        self.game_run = True

        while self.run and self.game_run: # mainloop ---------------------------------------------------------------- #
            self.clock.tick(self.FPS)
            print(self.clock.get_fps())

            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.run = False

                if event.type == pygame.MOUSEMOTION:

                    self.hovered_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))

                    self.setParallax()
                    if self.buy_menu_open:
                        buyMenu.hover(self)
                    elif self.turret_menu_open:
                        turretMenu.hover(self)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.selected_tile = list((math.floor(pos[0]/50)*50, math.floor(pos[1]/50)*50))

                    if self.buy_menu_open:
                        if buyMenu.operate(self):
                            self.turrets.append(eval(self.turret_string))
                    elif self.turret_menu_open:
                        turretMenu.operate(self)
                    elif self.selected_tile in self.turret_pos:
                        turretMenu.activate(self)
                    elif self.selected_tile in self.tiles:
                        buyMenu.activate(self)

            # sending enemies -------------------------------------------------------- #
            if self.enemy_send_timer > 0:
                self.enemy_send_timer -= 1
            else:
                self.enemies.append(eval(f"objects.{self.waves[self.wave][self.enemy_type_index][0]}(self.levels[self.level][0])"))
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

        self.gameOver()

    def setParallax(self):
        """
        Sets the parallax relative to mouse position
        :params pos: mouse position
        :returns: None
        """
        pos = pygame.mouse.get_pos()
        if self.parallax_mod > 0.02:
            self.parallax_move = [((self.resolution[0]//2-pos[0])/20)*self.parallax_mod, ((self.resolution[1]//2-pos[1])/15)*self.parallax_mod]

    def loadMusic(self, name, volume=0.1, looped=True, path="media/music/"):
        """
        Loads music and plays it
        :returns: None
        """
        pygame.mixer.music.load(f"{path}{name}")
        pygame.mixer.music.set_volume(volume)

        if looped:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    def loadLevel(self):
        """
        Loads level from levels.json, autofills the surrounding area around path
        :returns: None
        """
        self.health = 50
        self.money = 500
        self.wave = 0
        self.kills = 0
        self.enemy_send_timer = 300
        self.enemy_send_index = 0
        self.enemy_type_index = 0
        self.level += 1
        self.enemies = []
        self.tiles = []
        self.turrets = []
        self.turret_pos = []
        self.killed_enemies = []
        self.money_text = text_font_l.render(str(self.money)+" $", True, (255,255,255))
        self.health_text = text_font_l.render(str(self.health), True, (255,150,150))

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
                if tr.attackTarget(en):
                    break
                if en.health <= 0:
                    self.money += en.value
                    self.money_text = text_font_l.render(str(self.money)+" $", True, (255,255,255))
                    self.killed_enemies.append(en)
                    self.enemies.remove(en)
                    self.kills += 1
                    self.setParallax()

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
                self.health_text = text_font_l.render(str(self.health), True, (255,150,150))
                if self.health <= 0:
                    self.game_run = False

    def drawBoard(self):

        for en in self.killed_enemies: # explosions
            en.explode_2(self.Screen)
            if en.exploded_2_radius > self.resolution[0]:
                print(True)
                self.killed_enemies.remove(en)

        for p in self.levels[self.level]:
            if self.levels[self.level].index(p) == 0:
                self.Screen.blit(self.tile_sprites[3], (p[0], p[1], 50, 50))
            elif self.levels[self.level].index(p) == len(self.levels[self.level])-1:
                self.Screen.blit(self.tile_sprites[2], (p[0], p[1], 50, 50))
            else:
                self.Screen.blit(self.tile_sprites[1], (p[0], p[1], 50, 50))

        for t in self.tiles:
            self.Screen.blit(self.tile_sprites[0], (t[0], t[1], 50, 50))

        for en in self.enemies:
            en.draw(self.Screen)
        for tr in self.turrets:
            tr.draw(self.Screen)

        for en in self.killed_enemies: # explosions
            en.explode_1(self.Screen)

    def drawBg(self):
        """
        Draws the background image sliding to the left
        :returns: None
        """
        for bg in self.backgrounds:
            self.Screen.blit(bg[0],[bg[1][0]+self.parallax_move[0], bg[1][1]+self.parallax_move[1]])

            if bg[1][0] < -2*self.resolution[0]:
                self.backgrounds.append([self.bg, [self.resolution[0], -50]])
                self.backgrounds.remove(bg)
            if bg[1][0] > 2*self.resolution[0]:
                self.backgrounds.append([self.bg, [-self.resolution[0], -50]])
                self.backgrounds.remove(bg)

    def drawMenu(self):
        self.drawBg()

        self.Screen.blit(self.title_text, self.title_text_center)
        for button in self.main_menu_buttons:
            button.draw(self.Screen)

        self.drawBoard()

        pygame.display.update()

    def drawGameOver(self):
        """
        Draws game over
        :returns: None
        """
        self.drawBg()

        self.Screen.blit(self.game_over_text_1, self.game_over_text_1_center)
        self.Screen.blit(self.game_over_text_2, self.game_over_text_2_center)
        self.Screen.blit(self.game_over_stats, self.game_over_stats_center)
        self.try_again_button.draw(self.Screen)

        pygame.display.update()

    def drawCredits(self):
        """
        Draws credits when selected in mainMenu
        :returns: None
        """
        self.drawBg()
        self.Screen.blit(self.music_credits_text, [self.music_credits_text_center[0]+self.parallax_move[0]/2, self.music_credits_text_center[1]+self.parallax_move[1]/2])
        self.Screen.blit(self.art_credits_text, [self.art_credits_text_center[0]+self.parallax_move[0]/2, self.art_credits_text_center[1]+self.parallax_move[1]/2])
        self.Screen.blit(self.dev_credits_text, [self.dev_credits_text_center[0]+self.parallax_move[0]/2, self.dev_credits_text_center[1]+self.parallax_move[1]/2])

        pygame.display.update()

    def drawGame(self):
        """
        Draws all of the level elements except the background on the display, updates the display
        :returns: None
        """
        self.drawBg()
        self.drawBoard()

        # GUI
        if self.buy_menu_open:
            pygame.draw.rect(self.Screen, [100,100,100], (self.buy_menu_pos[0], self.buy_menu_pos[1], 50*self.buy_menu_width, 50))
            pygame.draw.rect(self.Screen, [80,80,80], (self.buy_menu_pos[0]+5, self.buy_menu_pos[1]+5, 50*self.buy_menu_width-10, 40))

            for tr in self.available_turrets:
                tr.draw(self.Screen)

            self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0]/7+25, self.COST_Y+self.parallax_move[1]/7))
            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0]/7+25, self.NOTIF_Y+self.parallax_move[1]/7))
            self.Screen.blit(self.cost_text, self.cost_center)
            self.Screen.blit(self.notif_text, self.notif_text_center)

        elif self.turret_menu_open:
            pygame.draw.rect(self.Screen, [100,100,100], (self.turret_menu_pos[0], self.turret_menu_pos[1], 50*self.turret_menu_width, 50))
            pygame.draw.rect(self.Screen, [80,80,80], (self.turret_menu_pos[0]+5, self.turret_menu_pos[1]+5, 50*self.turret_menu_width-10, 40))

            for btn in self.turret_menu_buttons:
                self.Screen.blit(btn[2],btn[1])

            self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0]/7+25, self.COST_Y+self.parallax_move[1]/7))
            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2+self.parallax_move[0]/7+25, self.NOTIF_Y+self.parallax_move[1]/7))
            self.Screen.blit(self.cost_text, self.cost_center)
            self.Screen.blit(self.notif_text, self.notif_text_center)

        self.Screen.blit(self.money_text, (30+self.parallax_move[0]/5,20+self.parallax_move[1]/5))
        self.Screen.blit(self.health_text, (30+self.parallax_move[0]/5,80+self.parallax_move[1]/5))
        if self.hovered_tile in self.tiles and not self.buy_menu_open and not self.turret_menu_open:
            self.Screen.blit(self.indicator, self.hovered_tile)

        pygame.display.update()


g = Game()
g.playIntro()

pygame.quit()

