import pygame
import math


class CircleAnimation:
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
        self.color = [x-self.substract if x > self.substract else x for x in self.color]


class BackgroundBeam:
    def __init__(self, velocities, init_color, default_length, start_pos, end_pos, width=1, multiplicate=1.04):
        self.default_length = default_length
        self.width = width
        self.color = init_color
        self.length = 0
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.x_v = velocities[0]/10
        self.y_v = velocities[1]/10

        self.multiplicate = multiplicate
        self.increment = 0.01

    def draw(self, display):
        pygame.draw.line(display, self.color, self.start_pos, self.end_pos, round(self.width))

    def modify(self):
        self.color = [x+0.5 if x < 255 else x for x in self.color]
        if self.length >= self.default_length:
            self.start_pos[0] += self.x_v * self.increment
            self.start_pos[1] += self.y_v * self.increment
            if self.increment < 1:
                self.increment += 0.01
        else:
            self.start_pos[0] += self.x_v * self.increment
            self.start_pos[1] += self.y_v * self.increment
            if self.increment < 1:
                self.increment += 0.01
        self.end_pos[0] += self.x_v
        self.end_pos[1] += self.y_v
        self.x_v = self.x_v*self.multiplicate
        self.y_v = self.y_v*self.multiplicate
        if self.width < 100:
            self.width += (self.width*0.08)**2
        self.length = math.hypot(self.start_pos[0]-self.end_pos[0], self.start_pos[1]-self.end_pos[1]) * 0.1
