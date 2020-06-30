import pygame


class Button:
    def __init__(self, color, pos_res, text, text_color, font, antialias=True):
        self.x = pos_res[0]
        self.y = pos_res[1]
        self.width = pos_res[2]
        self.height = pos_res[3]
        self.color = color
        self.default_color = color
        self.clicked_color = [x-40 for x in self.color if x >= 40]
        self.font = pygame.font.Font('media/other/Adobe Dia.ttf', font)
        self.text = self.font.render(text, antialias, text_color)
        self.text_center = self.text.get_rect(center=(self.width//2 + self.x, self.height//2 + self.y+5))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def draw(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height))
        display.blit(self.text, self.text_center)
