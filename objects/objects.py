from objects.abstract.enemy import Enemy
from objects.abstract.tower import Tower
from objects.abstract.button import Button
import pygame

pygame.init()
Screen = pygame.display.set_mode((800,600))

enemy_imgs = [
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_1.png").convert_alpha(), (20,20)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/circle_2.png").convert_alpha(), (25,25)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_1.png").convert_alpha(), (30,30)),
    pygame.transform.scale(pygame.image.load("sprites/enemies/square_2.png").convert_alpha(), (40,40)),
]

base_imgs = [pygame.image.load(f"sprites/towers/base/base_{x}.png") for x in range(1,4)]

# Enemies --------------------------------------------------------------------------- #
class Circle_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 25, 5, 5, 5, enemy_imgs[0])


class Circle_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 32, 10, 6, 15, enemy_imgs[1])


class Square_1(Enemy):
    def __init__(self, start):
        super().__init__(start, 40, 15, 7, 15, enemy_imgs[2])


class Square_2(Enemy):
    def __init__(self, start):
        super().__init__(start, 50, 20, 10, 20, enemy_imgs[3])


# Turrets --------------------------------------------------------------------------- #
class Kinetic_1(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 125
        else:
            range_ = 0
        super().__init__(pos, 5, 250, base_imgs[0], level, range_, 60, 1)
        self.description = "Easily affordable"


class Kinetic_2(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 150
        else:
            range_ = 0
        super().__init__(pos, 0.5, 500, base_imgs[1], level, range_, 10, 0.5)
        self.description = "Fast shooting"


class Kinetic_3(Tower):
    def __init__(self, pos, active, level=0):
        if active:
            range_ = 175
        else:
            range_ = 0
        super().__init__(pos, 15, 1000, base_imgs[2], level, range_, 90, 1.5)
        self.description = "Heavy artillery"


# Buttons --------------------------------------------------------------------------- #
class newGameButton(Button):
    def __init__(self, pos_res):
        super().__init__([50,125,50], pos_res, "New Game", [255,255,255], 90)


class creditsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Credits", [255,255,255], 90)


class settingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Settings", [255,255,255], 90)


class audioSettingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Audio Settings", [255,255,255], 110)


class videoSettingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Video Settings", [255,255,255], 110)


class backSettingsButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Back", [255,255,255], 90)


class tryAgainButton(Button):
    def __init__(self, pos_res):
        super().__init__([75,75,75], pos_res, "Main Menu", [255,255,255], 90)
