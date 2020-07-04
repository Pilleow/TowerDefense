import pygame
from random import randint

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

NOTIF_Y = 100
COST_Y = 50

text_font_l = pygame.font.Font('media/other/Adobe Dia.ttf', 90)
text_font_m = pygame.font.Font('media/other/Adobe Dia.ttf', 70)
text_font_s = pygame.font.Font('media/other/Adobe Dia.ttf', 50)

def hover(self):
    """
    Handles changing text when mouse is hovering over an active buyMenu
    :params self: class 'self'
    :returns: None
    """
    if self.buy_menu_open:
        for tr in self.available_turrets:
            if self.hovered_tile != tr.pos:
                continue

            self.cost_text = text_font_m.render(str(tr.cost)+" $", True, (255,255,255))
            if self.money >= tr.cost:
                self.notif_text = text_font_s.render(tr.description, True, (100,255,100))
                continue

            self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
            break

def operate(self):
    """
    Handles closing and mouse clicking for a buyMenu
    :params self: class 'self'
    :returns: True if turret selected for buy, False if otherwise
    """
    if self.selected_tile[0] < self.buy_menu_pos[0] or self.selected_tile[0] > self.buy_menu_pos[0] + 50*(self.buy_menu_width-1) or self.selected_tile[1] < self.buy_menu_pos[1] or self.selected_tile[1] > self.buy_menu_pos[1]:
        self.cost_text = text_font_m.render(" ", True, (255,255,255))
        self.notif_text = text_font_s.render(" ", True, (255,100,100))
        self.buy_menu_open = False

    else:
        for tr in self.available_turrets:
            if tr.pos != self.selected_tile:
                continue

            if self.money >= tr.cost:
                pos = [self.buy_menu_pos[0]-50, self.buy_menu_pos[1]]
                self.turret_pos.append(pos)
                self.buy_menu_open = False
                self.money -= tr.cost
                self.money_text = text_font_l.render(str(self.money)+" $", True, (255,255,255))
                self.cost_text = text_font_m.render(" ", True, (255,255,255))
                self.notif_text = text_font_s.render(" ", True, (100,255,100))
                self.turret_string = f"objects.{tr.__class__.__name__}({pos}, True)"
                self.sfx[f"shop_{randint(0,2)}"].play()
                return True
            return False

def activate(self):
    """
    Handles opening for a buyMenu
    :params self: class 'self'
    :returns: None
    """
    self.buy_menu_open = True
    self.buy_menu_pos = [self.selected_tile[0] + 50, self.selected_tile[1]]

    self.cost_text = text_font_m.render(" ", True, (255,255,255))
    self.notif_text = text_font_s.render(" ", True, (255,100,100))

    count = 0
    for tr in self.available_turrets:
        tr.__init__([self.buy_menu_pos[0] + 50 * count, self.buy_menu_pos[1]], False)
        count += 1
