import pygame
import math
from random import randint

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

Screen = pygame.display.set_mode((800, 600))

turret_imgs = [pygame.image.load(f"sprites/towers/head/level_{x}.png").convert_alpha() for x in range(0, 5)]
support_base_imgs = [pygame.image.load(f'sprites/towers/base/support/level_{x}.png') for x in range(1,5)]


class Tower:
    def __init__(self, pos, dmg, cost, base_sprite, level, range_, shoot_cooldown, beam_thickness, active):
        if active:
            self.info_range = range_
        else:
            self.info_range = 0
        self.range_ = range_
        self.pos = pos
        self.dmg = dmg
        self.cost = cost
        self.level = level
        self.max_level = len(turret_imgs) - 1
        self.turret_sprite = turret_imgs[self.level+1]
        self.x_offset = self.turret_sprite.get_rect().size[0] // 2
        self.y_offset = self.turret_sprite.get_rect().size[1] // 2
        self.x = pos[0] + 25 - self.x_offset
        self.y = pos[1] + 25 - self.y_offset
        self.shoot_cooldown_d = shoot_cooldown
        self.shoot_cooldown = 0
        self.base_sprite = base_sprite
        self.base_center = self.base_sprite.get_rect(center=(pos[0] + 25, pos[1] + 25))
        self.target = None
        self.beam_drawtime = 0
        self.beam_modifier = beam_thickness
        self.show_range = False

    def upgrade(self):
        if self.level >= self.max_level:
            return False

        self.level += 1
        self.turret_sprite = turret_imgs[self.level]
        self.dmg += 1
        self.shoot_cooldown_d -= 1 * round(self.shoot_cooldown_d / 10) - 1
        self.range_ += 15
        self.cost += round(self.cost * 0.5)
        return True

    def attack_target(self, enemy):
        """
        Checks if 'enemy' is in range and if True, shoots it
        :params enemy: Enemy object
        :returns: True if enemy found and if enemy shot
        """
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        if distance <= self.range_ and self.shoot_cooldown <= 0:
            self.shoot_cooldown = randint(self.shoot_cooldown_d - 2, self.shoot_cooldown_d + 2)
            enemy.health -= self.dmg
            self.target = (round(enemy.x + enemy.x_offset), round(enemy.y + enemy.y_offset))
            self.beam_drawtime = 7
            return True
        return False

    def draw(self, display, mode=0):
        display.blit(self.base_sprite, self.base_center)

        if self.beam_drawtime:  # drawing turret beam when shooting
            pygame.draw.line(display, (225, 225, 225), (self.x + self.x_offset, self.y + self.y_offset), self.target,
                             round(self.beam_modifier * self.beam_drawtime))
            self.beam_drawtime -= 0.5

        display.blit(self.turret_sprite, (self.x, self.y))

        if self.range_ > 0 and self.show_range:
            pygame.draw.circle(display, (200, 200, 200), (self.pos[0] + 25, self.pos[1] + 25), self.range_, 2)


class SupportTower:
    def __init__(self, pos, cost, level, range_, active, effects):
        if active:
            self.info_range = range_
        else:
            self.info_range = 0
        self.range_ = range_
        self.pos = pos
        self.cost = cost
        self.level = level
        self.max_level = len(support_base_imgs) - 1
        self.turret_sprite = turret_imgs[0]
        self.x_offset = self.turret_sprite.get_rect().size[0] // 2
        self.y_offset = self.turret_sprite.get_rect().size[1] // 2
        self.x = pos[0] + 25 - self.x_offset
        self.y = pos[1] + 25 - self.y_offset
        self.base_sprite = support_base_imgs[self.level]
        self.base_center = self.base_sprite.get_rect(center=(pos[0] + 25, pos[1] + 25))
        self.target = None
        self.show_range = False
        self.effects = effects

    def upgrade(self):
        if self.level >= self.max_level:
            return False

        self.level += 1
        self.base_sprite = support_base_imgs[self.level]
        self.range_ += 15
        self.cost += round(self.cost * 0.5)
        return True

    def draw(self, display):
        display.blit(self.base_sprite, self.base_center)
        display.blit(self.turret_sprite, (self.x, self.y))

        if self.range_ > 0 and self.show_range:
            pygame.draw.circle(display, (200, 200, 200), (self.pos[0] + 25, self.pos[1] + 25), self.range_, 2)