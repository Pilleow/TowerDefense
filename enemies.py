from obj.enemy import Enemy
import pygame

class Circle_1(Enemy):
    def __init__(self):
        super().__init__(5, 10, 5)
        self.sprite = pygame.image.load("sprites/enemies/circle_1.png").convert_alpha()

class Circle_2(Enemy):
    def __init__(self):
        super().__init__(5, 10, 5)
        self.sprite = pygame.image.load("sprites/enemies/circle_2.png").convert_alpha()

class Square_1(Enemy):
    def __init__(self):
        super().__init__(5, 10, 5)
        self.sprite = pygame.image.load("sprites/enemies/square_1.png").convert_alpha()

class Square_2(Enemy):
    def __init__(self):
        super().__init__(5, 10, 5)
        self.sprite = pygame.image.load("sprites/enemies/square_2.png").convert_alpha()
