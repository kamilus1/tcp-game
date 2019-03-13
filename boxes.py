import pygame
from random import randint

class BoxesTypes:
    @classmethod
    def hp_box(cls, hp):
        hp += 2
        return hp

    @classmethod
    def speed_box(cls, speed):
        speed += 0.5
        return speed

    @classmethod
    def ouch_box(cls, hp):
        if hp > 2:
            hp -= 2
        return hp

    @classmethod
    def dmg_box(cls, dmg):
        dmg += 1
        return dmg
    @classmethod
    def no_dmg_box(cls, dmg):
        if dmg > 2:
            dmg -= 1
        return dmg
    @classmethod
    def xp_box(cls, xp, lvl):
        xp += randint(5*lvl, 10*lvl)
        return xp
    @classmethod
    def lucky_box(cls, chance):
        chance += 1
        return chance

    @classmethod
    def unlucky_box(cls, chance):
        if chance > 1:
            chance -= 1
        return chance
class Box(object):
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        types = BoxesTypes()
        self.events = [types.hp_box, types.speed_box, types.ouch_box, types.dmg_box, types.no_dmg_box, types.xp_box, types.lucky_box, types.unlucky_box]

    def showBox(self, screen, x, y):
        self.x1 = x
        self.y1 = y
        pygame.draw.rect(screen, (60, 90, 220), (x, y, 50, 50))
    def effect(self, hp=None, dmg=None, speed=None, mana=None,xp=None, lvl=None, chan=None):
        x = randint(0, len(self.events))
        if x == 0:
            hp = self.events[x](hp)
        elif x == 1:
            speed = self.events[x](speed)
        elif x == 2:
            hp = self.events[x](hp)
        elif x == 3:
            dmg = self.events[x](dmg)
        elif x == 4:
            dmg = self.events[x](dmg)
        elif x==5:
            xp = self.events[x](xp, lvl)
        elif x==6:
            chan = self.events[x](chan)
        elif x==7:
            chan = self.events[x](chan)
        return hp, dmg, speed, mana, xp, chan

