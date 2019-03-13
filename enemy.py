import pygame
from random import randint
from hero import Hero
class Enemy(Hero):
    def __init__(self, color, screen):
        Hero.__init__(self, color, screen)
        self.dmg = randint(1, 7)
        self.hp = randint(1, 8)
    def display(self, x, y, name="enemy"):
        Hero.display(self, x, y, name)
    def attack(self, hp):
        hp -= self.dmg
        return hp
    def get_shot(self, dmg):
        self.hp -= dmg