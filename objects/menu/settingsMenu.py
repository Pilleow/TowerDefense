import pygame
import json

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

text_font_xl = pygame.font.Font('media/other/Adobe Dia.ttf', 160)
text_font_l = pygame.font.Font('media/other/Adobe Dia.ttf', 120)
text_font_m = pygame.font.Font('media/other/Adobe Dia.ttf', 80)

def settings_active(self):
    """
    Main loop, runs when settings are selected
    :returns: None
    """
    self.main_title = text_font_xl.render("Settings", True, (255,255,255))

    settings_main_open = True

    self.main_title_center = self.main_title.get_rect(center=(self.resolution[0]/2, self.resolution[1]/5.7))

    while settings_main_open and self.run: # mainloop ---------------------------------------------------------------- #
        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.setParallax(pos)

                for button in self.settings_buttons:
                    if button.isOver(pos):
                        button.color = button.clicked_color
                    else:
                        button.color = button.default_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.settings_buttons[0].isOver(pos): # audio
                    self.settings_buttons[0].color = self.settings_buttons[0].default_color
                    self.sfx['menu_nav'].play()
                    audio_settings(self)

                elif self.settings_buttons[1].isOver(pos): # video
                    self.settings_buttons[1].color = self.settings_buttons[1].default_color
                    self.sfx['menu_nav'].play()
                    video_settings(self)

                elif self.settings_buttons[2].isOver(pos): # back
                    self.settings_buttons[2].color = self.settings_buttons[2].default_color
                    self.sfx['menu_nav'].play()
                    settings_main_open = False

        if self.run:
            draw_main_settings(self)

def video_settings(self):
    """
    Main loop, runs when video settings are selected
    :returns: None
    """
    self.video_title = text_font_l.render("Video Settings", True, (255,255,255))
    mouse_left_holding = False
    settings_video_open = True

    self.video_title_center = self.video_title.get_rect(center=(self.resolution[0]/2, self.resolution[1]/5))

    while settings_video_open and self.run: # mainloop ---------------------------------------------------------------- #
        self.clock.tick(self.FPS)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEMOTION:
                self.setParallax(pos)

                for button in self.settings_buttons:
                    if button.isOver(pos):
                        button.color = button.clicked_color
                    else:
                        button.color = button.default_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_left_holding = True

                if self.settings_buttons[2].isOver(pos): # back
                    self.settings_buttons[2].color = self.settings_buttons[2].default_color
                    self.sfx['menu_nav'].play()
                    settings_video_open = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_left_holding = False

        draw_video_settings(self, pos, mouse_left_holding)

def audio_settings(self):
    """
    Main loop, runs when audio settings are selected
    :returns: None
    """
    self.audio_title = text_font_l.render("Audio Settings", True, (255,255,255))
    self.music_vol_text = text_font_m.render("Music Volume", True, (250,250,250))
    self.sfx_vol_text = text_font_m.render("SFX Volume", True, (250,250,250))

    self.audio_title_center = self.audio_title.get_rect(center=(self.resolution[0]/2, self.resolution[1]/5))

    mouse_left_holding = False
    settings_audio_open = True

    while settings_audio_open and self.run: # mainloop ---------------------------------------------------------------- #
        self.clock.tick(self.FPS)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEMOTION:
                self.setParallax(pos)

                for button in self.settings_buttons:
                    if button.isOver(pos):
                        button.color = button.clicked_color
                    else:
                        button.color = button.default_color

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_left_holding = True

                if self.settings_buttons[2].isOver(pos): # back
                    self.settings_buttons[2].color = self.settings_buttons[2].default_color
                    self.sfx['menu_nav'].play()
                    settings_audio_open = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_left_holding = False

        draw_audio_settings(self, pos, mouse_left_holding)

    with open('data/settings.json') as f: # saving audio settings
        settings = json.load(f)
        settings['music_volume'] = self.music_volume
        settings['sfx_volume'] = self.sfx_volume

    with open('data/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    for key in self.sfx:
        self.sfx[key].set_volume(self.sfx_volume)

def slider(self, mouse_pos, type_, mouse_left_holding, pos_res, color=[250,250,250]):
    """
    Draws a slider
    :returns: None
    """
    if type_ == 'music':
        slider_width = pos_res[2]*self.music_volume
    if type_ == 'sfx':
        slider_width = pos_res[2]*self.sfx_volume

    if mouse_left_holding:
        if mouse_pos[0] > pos_res[0] and mouse_pos[0] < pos_res[0]+pos_res[2] and mouse_pos[1] >= pos_res[1] and mouse_pos[1] <= pos_res[1]+pos_res[3]:

            slider_width = mouse_pos[0] - pos_res[0]

            if type_ == 'music':
                self.music_volume = (mouse_pos[0] - pos_res[0])/pos_res[2]
                pygame.mixer.music.set_volume(self.music_volume)

            if type_ == 'sfx':
                self.sfx_volume = (mouse_pos[0] - pos_res[0])/pos_res[2]

    pygame.draw.rect(self.Screen, color, pos_res)
    pygame.draw.rect(self.Screen, [44,44,44], [ pos_res[0]+2, pos_res[1]+2, pos_res[2]-4, pos_res[3]-4 ])
    pygame.draw.rect(self.Screen, color, [ pos_res[0], pos_res[1], slider_width, pos_res[3] ])

def draw_main_settings(self):
    """
    Drawing the contents of main settings menu
    :returns: None
    """
    self.drawBg()

    self.Screen.blit(self.main_title, self.main_title_center)

    for button in self.settings_buttons:
        button.draw(self.Screen)

    pygame.display.update()

def draw_audio_settings(self, mouse_pos, mouse_left_holding):
    """
    Drawing the contents of audio settings menu
    :returns: None
    """
    self.drawBg()
    self.Screen.blit(self.audio_title, self.audio_title_center)

    self.Screen.blit(self.music_vol_text, [ self.resolution[0]/2-400, self.resolution[1]/2 - 150 ]) # music volume
    slider(self, mouse_pos, 'music', mouse_left_holding, [ self.resolution[0]/2-400, self.resolution[1]/2-75, 800, 50 ])

    self.Screen.blit(self.sfx_vol_text, [ self.resolution[0]/2-400, self.resolution[1]/2 ]) # sfx volume
    slider(self, mouse_pos, 'sfx', mouse_left_holding, [ self.resolution[0]/2-400, self.resolution[1]/2+75, 800, 50 ])

    self.settings_buttons[2].draw(self.Screen)

    pygame.display.update()

def draw_video_settings(self, mouse_pos, mouse_left_holding):
    """
    Drawing the contents of video settings menu
    :returns: None
    """
    self.drawBg()

    self.Screen.blit(self.video_title, self.video_title_center)

    self.settings_buttons[2].draw(self.Screen)

    pygame.display.update()
