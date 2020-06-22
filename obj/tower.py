import pygame


class Tower:
    def __init__(self, pos, dmg, cost, sprite):
        self.pos = pos
        self.x = pos[0]+25-sprite.get_rect().size[0]//2
        self.y = pos[1]+25-sprite.get_rect().size[1]//2
        self.dmg = dmg
        self.cost = cost
        self.sprite = sprite # head of a turret
        self.bases = [pygame.image.load(f"sprites/towers/base/base_{x}.png") for x in range(1,4)]
        self.base_level = 0
        self.base_center = self.bases[self.base_level].get_rect(center=(pos[0]+25, pos[1]+25))

    def draw(self, display):
        display.blit(self.bases[0], self.base_center)
        display.blit(self.sprite, (self.x, self.y))
