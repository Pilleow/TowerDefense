import pygame
import math
pygame.init()
Screen = pygame.display.set_mode((800,600))

turret_imgs = [pygame.transform.scale(pygame.image.load(f"sprites/towers/head/level_{x}.png").convert_alpha(), (20,20)) for x in range(1,5)]


class Tower:
    def __init__(self, pos, dmg, cost, base_sprite, level, range_, shoot_cooldown, beam_thickness):
        self.pos = pos
        self.range_ = range_
        self.dmg = dmg
        self.cost = cost
        self.level = level
        self.turret_sprite = turret_imgs[self.level]
        self.x_offset = self.turret_sprite.get_rect().size[0]//2
        self.y_offset = self.turret_sprite.get_rect().size[1]//2
        self.x = pos[0]+25-self.x_offset
        self.y = pos[1]+25-self.y_offset
        self.shoot_cooldown_default = shoot_cooldown
        self.shoot_cooldown = 0
        self.base_sprite = base_sprite
        self.base_center = self.base_sprite.get_rect(center=(pos[0]+25, pos[1]+25))
        self.target = None
        self.beam_drawtime = 0
        self.beam_modifier = beam_thickness
        self.show_range = False

    def upgrade(self):
        if self.level >= len(turret_imgs)-1:
            return False

        self.level += 1
        self.turret_sprite = turret_imgs[self.level]
        self.dmg += 1 + 1*self.level-1
        self.shoot_cooldown_default -= 1 * self.shoot_cooldown_default/10 - 1
        self.range_ += 5
        self.cost += round(self.cost*0.5)
        return True

    def attackTarget(self, enemy):
        """
        Checks if 'enemy' is in range and if True, shoots it
        :params enemy: Enemy object
        :returns: True if enemy found and if enemy shot
        """
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        if distance <= self.range_ and self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_cooldown_default
            enemy.health -= self.dmg
            self.target = (round(enemy.x+enemy.x_offset), round(enemy.y+enemy.y_offset))
            self.beam_drawtime = 7
            return True
        return False

    def draw(self, display, mode=0):
        display.blit(self.base_sprite, self.base_center)

        if self.beam_drawtime: # drawing turret beam when shooting
            pygame.draw.line(display, (225,225,225), (self.x+self.x_offset, self.y+self.y_offset), self.target, round(self.beam_modifier * self.beam_drawtime))
            self.beam_drawtime -= 1
        display.blit(self.turret_sprite, (self.x, self.y))

        if self.range_ > 0 and self.show_range:
            pygame.draw.circle(display, (200,255,200), (self.pos[0]+25, self.pos[1]+25), self.range_, 2)
