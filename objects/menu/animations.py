import pygame

class circleAnimation:
    def __init__(self, color, pos, width=25, radius=50, increment=2, substract=1, multiplicate=1.05):
        self.color = color
        self.width = width
        self.radius = radius
        self.pos = pos
        self.increment = increment
        self.substract = substract
        self.multiplicate = multiplicate

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.radius, self.width)
        self.radius += round(self.increment)
        self.increment = self.increment * self.multiplicate
        self.color = [ x-self.substract if x > self.substract else x for x in self.color ]
