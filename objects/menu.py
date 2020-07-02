import pygame

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

text_font_m = pygame.font.Font('media/other/Adobe Dia.ttf', 70)
text_font_s = pygame.font.Font('media/other/Adobe Dia.ttf', 50)

# BUY MENU -------------------------------------------------------------------------------------------------------------- #
def buyMenuHover(self):
    """
    Handles changing text when mouse is hovering over an active buyMenu
    :params self: class 'self'
    :returns: None
    """
    if self.buy_menu_open: # handling buyMenu text
        for tr in self.available_turrets:
            if self.hovered_tile != tr.pos:
                continue

            self.cost_text = text_font_m.render(str(tr.cost)+" $", True, (255,255,255))
            self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))
            if self.money >= tr.cost:
                self.notif_text = text_font_s.render(tr.description, True, (100,255,100))
                self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
                continue

            self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
            break

def buyMenuActive(self):
    """
    Handles opening, closing and mouse clicking for a buyMenu
    :params self: class 'self'
    :returns: None
    """
    if self.buy_menu_open: # handling buyMenu
        if selected_tile[0] < self.buy_menu_pos[0] or selected_tile[0] > self.buy_menu_pos[0] + 50*(self.buy_menu_width-1) or selected_tile[1] < self.buy_menu_pos[1] or selected_tile[1] > self.buy_menu_pos[1]:
            self.cost_text = text_font_m.render(" ", True, (255,255,255))
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
                    self.cost_text = text_font_m.render(" ", True, (255,255,255))
                    self.notif_text = text_font_s.render(" ", True, (100,255,100))
                    self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
                break

    elif selected_tile in self.tiles: # opening buyMenu
        self.buy_menu_open = True
        self.buy_menu_pos = [selected_tile[0] + 50, selected_tile[1]]

        count = 0
        for tr in self.available_turrets:
            tr.__init__([self.buy_menu_pos[0] + 50 * count, self.buy_menu_pos[1]], False)
            count += 1

# TURRET MENU ----------------------------------------------------------------------------------------------------------- #
def turretMenuHover(self):
    """
    Handles changing text when mouse is hovering over an active turretMenu
    :params self: class 'self'
    :returns: None
    """
    if self.turret_menu_open: # handling turretMenu text
        for btn in self.turret_menu_buttons:
            if self.hovered_tile != [btn[1][0]-5, btn[1][1]-5]:
                continue

            if btn[0] == 'sell':
                self.notif_text = text_font_s.render("80% Refund", True, (100,255,100))
                self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
                self.cost_text = text_font_m.render(str(round(self.selected_turret.cost * 0.8))+" $", True, (255,255,255))
                self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))
                break

            else:
                if self.selected_turret.level >= self.selected_turret.max_level:
                    self.notif_text = text_font_s.render(" ", True, (255,100,100))
                    self.cost_text = text_font_m.render("Maxed out", True, (255,255,255))
                    self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))
                    continue

                self.cost_text = text_font_m.render(str(self.selected_turret.cost // 2)+" $", True, (255,255,255))
                self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))

                if self.money >= self.selected_turret.cost // 2:
                    self.notif_text = text_font_s.render(" ", True, (255,100,100))
                    continue

                self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
                self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
                break

def turretMenuActive(self):
    if self.turret_menu_open: # handling turretMenu
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
                            if self.selected_turret.level >= self.selected_turret.max_level:
                                self.notif_text = text_font_s.render(" ", True, (255,100,100))
                                self.cost_text = text_font_m.render("Maxed out", True, (255,255,255))
                                self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))
                                continue

                            self.money -= round(prev_cost*0.5)
                            self.money_text = text_font_m.render(str(self.money)+" $", True, (255,255,255))

                            self.cost_text = text_font_m.render(str(round(self.selected_turret.cost * 0.5))+" $", True, (255,255,255))
                            self.cost_center = self.cost_text.get_rect(center=(self.resolution[0]//2, 35))
                            if self.money >= self.selected_turret.cost // 2:
                                self.notif_text = text_font_s.render(" ", True, (255,100,100))
                                continue

                            self.notif_text = text_font_s.render("Not enough money!", True, (255,100,100))
                            self.notif_text_center = self.notif_text.get_rect(center=(self.resolution[0]//2, 75))
                            break
                break

    elif selected_tile in self.turret_pos: # opening turretMenu
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
