import pygame

base_imgs = [pygame.transform.scale(pygame.image.load(f"sprites/towers/base/base_{x}.png"),(40,40)) for x in range(1,4)]

class Tower:
    def __init__(self, pos, dmg, cost, sprite, level, range_, shoot_cooldown):
        self.pos = pos
        self.x = pos[0]+25-sprite.get_rect().size[0]//2
        self.y = pos[1]+25-sprite.get_rect().size[1]//2
        self.range_ = range_
        self.dmg = dmg
        self.cost = cost
        self.sprite = sprite # head of a turret
        self.level = level
        self.shoot_cooldown_default = shoot_cooldown
        self.shoot_cooldown = 0
        self.base_center = base_imgs[self.level].get_rect(center=(pos[0]+25, pos[1]+25))

    def draw(self, display):
        display.blit(base_imgs[self.level], self.base_center)
        display.blit(self.sprite, (self.x, self.y))
        if self.range_ > 0:
            pygame.draw.circle(display, (255,255,255), (self.pos[0]+25, self.pos[1]+25), self.range_, 3)
