import pygame
from random import randint

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

COST_Y = 50
NOTIF_Y = 100

text_font_l = pygame.font.Font('media/other/Adobe Dia.ttf', 90)
text_font_m = pygame.font.Font('media/other/Adobe Dia.ttf', 70)
text_font_s = pygame.font.Font('media/other/Adobe Dia.ttf', 50)


def hover(self):
    """
    Handles changing text when mouse is hovering over an active turretMenu
    :params self: class 'self'
    :returns: None
    """
    for btn in self.turret_menu_buttons:
        if self.selected_tile != [btn[1][0] - 5, btn[1][1] - 5]:
            continue

        if btn[0] == 'sell':
            self.notif_text = text_font_s.render("80% Refund", True, (100, 255, 100))
            self.cost_text = text_font_l.render(str(round(self.selected_turret.cost * 0.8)) + " $", True,
                                                (255, 255, 255))
            break

        else:
            if self.selected_turret.level >= self.selected_turret.max_level:
                self.notif_text = text_font_s.render(" ", True, (255, 100, 100))
                self.cost_text = text_font_l.render("Maxed out", True, (255, 255, 255))
                continue

            self.cost_text = text_font_l.render(str(self.selected_turret.cost // 2) + " $", True, (255, 255, 255))

            if self.money >= self.selected_turret.cost // 2:
                self.notif_text = text_font_s.render(" ", True, (255, 100, 100))
                continue

            self.notif_text = text_font_s.render("Not enough money!", True, (255, 100, 100))
            break


def operate(self):
    if self.selected_tile[0] < self.turret_menu_pos[0] or self.selected_tile[0] > self.turret_menu_pos[0] + 50 * (
            self.turret_menu_width - 1) or self.selected_tile[1] < self.turret_menu_pos[1] or self.selected_tile[1] > \
            self.turret_menu_pos[1]:
        self.turret_menu_open = False
        self.selected_turret.show_range = False

    else:
        for btn in self.turret_menu_buttons:
            if [btn[1][0] - 5,
                btn[1][1] - 5]\
                    != self.selected_tile:  # btn[2] = sprite; btn[1] = position; btn[0] = type
                continue

            if btn[0] == 'sell':
                self.money += round(self.selected_turret.cost * 0.8)
                self.money_text = text_font_m.render(str(self.money) + " $", True, (255, 255, 255))

                if self.selected_turret.type == 'support':
                    self.apply_support(self.selected_turret, True)
                    self.support.remove(self.selected_turret)
                elif self.selected_turret.type == 'attack':
                    self.turrets.remove(self.selected_turret)

                self.turret_pos.remove(self.selected_turret.pos)
                self.selected_turret.show_range = False
                self.turret_menu_open = False
                self.sfx[f"shop_{randint(0, 2)}"].play()
                break

            elif btn[0] == 'upgrade':
                if self.money >= self.selected_turret.cost * 0.5:
                    prev_cost = self.selected_turret.cost

                    for sp in self.support:  # resetting the applied support upgrades
                        self.apply_support(sp, True)

                    if self.selected_turret.upgrade(): # upgrading turret in upgrade()

                        for sp in self.support:  # resetting the applied support upgrades
                            self.apply_support(sp)

                        if self.selected_turret.level >= self.selected_turret.max_level:
                            self.notif_text = text_font_s.render(" ", True, (255, 100, 100))
                            self.cost_text = text_font_l.render("Maxed out", True, (255, 255, 255))
                            continue

                        self.money -= round(prev_cost * 0.5)
                        self.sfx[f"shop_{randint(0, 2)}"].play()
                        self.money_text = text_font_m.render(str(self.money) + " $", True, (255, 255, 255))

                        self.cost_text = text_font_l.render(str(round(self.selected_turret.cost * 0.5)) + " $", True,
                                                            (255, 255, 255))
                        if self.money >= self.selected_turret.cost // 2:
                            self.notif_text = text_font_s.render(" ", True, (255, 100, 100))
                            continue

                        self.notif_text = text_font_s.render("Not enough money!", True, (255, 100, 100))
                        break

                    for sp in self.support:  # resetting the applied support upgrades
                        self.apply_support(sp)
            break


def activate(self):
    self.turret_menu_open = True
    self.turret_menu_pos = [self.selected_tile[0] + 50, self.selected_tile[1]]

    self.cost_text = text_font_l.render(" ", True, (255, 255, 255))
    self.notif_text = text_font_s.render(" ", True, (255, 100, 100))

    count = 0
    for btn in self.turret_menu_buttons:
        btn[1][0] = self.turret_menu_pos[0] + 50 * count + 5
        btn[1][1] = self.turret_menu_pos[1] + 5
        count += 1

    for tr in self.turrets + self.support:
        if tr.pos != self.selected_tile:
            continue

        self.selected_turret = tr
        self.selected_turret.show_range = True
        break
