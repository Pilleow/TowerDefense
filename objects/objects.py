from objects.abstract.enemy import Enemy
from objects.abstract.tower import Tower, SupportTower
from objects.abstract.button import Button
import pygame

pygame.init()
Screen = pygame.display.set_mode((800, 600))

enemy_imgs = [
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_1.png").convert_alpha(), (20, 20)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_2.png").convert_alpha(), (25, 25)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_1.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_2.png").convert_alpha(), (40, 40)),
]

base_imgs = [pygame.image.load(f"sprites/towers/base/base_{x}.png") for x in range(1, 4)]
support_imgs = [pygame.image.load(f"sprites/towers/head/support/head_{x}.png") for x in range(1, 1)]
# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        self.id = 0
        super().__init__(start, 25, 5, 5, 5, enemy_imgs[0])


class Circle_2(Enemy):
    def __init__(self, start):
        self.id = 1
        super().__init__(start, 32, 10, 6, 5, enemy_imgs[1])


class Square_1(Enemy):
    def __init__(self, start):
        self.id = 2
        super().__init__(start, 40, 15, 7, 10, enemy_imgs[2])


class Square_2(Enemy):
    def __init__(self, start):
        self.id = 3
        super().__init__(start, 50, 20, 10, 10, enemy_imgs[3])


# Turrets --------------------------------------------------------------------------- #
class Kinetic_1(Tower):
    def __init__(self, pos, active, level=0):
        self.description = "Easily affordable"
        self.id = 0
        self.type = 'attack'
        super().__init__(pos, 5, 250, base_imgs[0], level, 125, 60, 1, active)


class Kinetic_2(Tower):
    def __init__(self, pos, active, level=0):
        self.description = "Fast shooting"
        self.id = 1
        self.type = 'attack'
        super().__init__(pos, 0.5, 500, base_imgs[1], level, 150, 15, 0.5, active)


class Kinetic_3(Tower):
    def __init__(self, pos, active, level=0):
        self.description = "Heavy artillery"
        self.id = 2
        self.type = 'attack'
        super().__init__(pos, 15, 1000, base_imgs[2], level, 175, 90, 1.5, active)


class Support_1(SupportTower):
    def __init__(self, pos, active, level=0):
        self.description = "Support unit"
        self.id = 2
        self.type = 'support'
        effects = {
            "range": 25,
            "dmg": 0,
            "shoot_cooldown_d": 0
        }
        self.info = "+25 range to nearby units"
        super().__init__(pos, 250, level, 150, active, effects)


class Support_2(SupportTower):
    def __init__(self, pos, active, level=0):
        self.description = "Support unit"
        self.id = 2
        self.type = 'support'
        effects = {
            "range": 0,
            "dmg": 1,
            "shoot_cooldown_d": 0
        }
        self.info = "+1 damage to nearby units"
        super().__init__(pos, 250, level, 150, active, effects)


class Support_3(SupportTower):
    def __init__(self, pos, active, level=0):
        self.description = "Support unit"
        self.id = 2
        self.type = 'support'
        effects = {
            "range": 0,
            "dmg": 0,
            "shoot_cooldown_d": -5
        }
        self.info = "+5 rate of fire to nearby units"
        super().__init__(pos, 250, level, 150, active, effects)


# Buttons --------------------------------------------------------------------------- #
class newGameButton(Button):
    def __init__(self, pos_res):
        super().__init__([50, 125, 50], pos_res, "New Game", [255, 255, 255], 90)


class creditsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Credits", [255, 255, 255], 90)


class settingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Settings", [255, 255, 255], 90)


class audioSettingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Audio Settings", [255, 255, 255], 110)


class videoSettingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Video Settings", [255, 255, 255], 110)


class backButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Back", [255, 255, 255], 90)


class tryAgainButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 75], pos_res, "Main Menu", [255, 255, 255], 90)


class resumeButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 150, 75], pos_res, "Resume", [255, 255, 255], 90)


class menuButton(Button):
    def __init__(self, pos_res):
        super().__init__([150, 75, 75], pos_res, "Surrender", [255, 255, 255], 90)


class playLevelButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 150, 75], pos_res, "Launch!", [255, 255, 255], 90)


class nextLevelButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 100], pos_res, "Next", [255, 255, 255], 90)


class prevLevelButton(Button):
    def __init__(self, pos_res):
        super().__init__([75, 75, 100], pos_res, "Prev", [255, 255, 255], 90)
