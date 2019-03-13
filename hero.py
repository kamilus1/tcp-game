import pygame
from math import sqrt, pow
class Hero:
    def __init__(self, color, screen):
        self.screen = screen
        self.color = color
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", 15)
    def display(self, x, y, name=""):
        pygame.draw.rect(self.screen, self.color, (x, y, 50, 50))
        text = self.font.render(name, True, (200, 200, 200))
        y1 = y-20
        x1 = x
        x1 *= 2
        x1 += 50
        x1 /= 2
        x1 -= text.get_width()/2
        self.screen.blit(text, (x1, y1))

    def shoot(self, x, y):
        self.lineX = pygame.mouse.get_pos()[0] - x
        self.lineY = pygame.mouse.get_pos()[1] - y
        self.pitagoras = sqrt(pow(self.lineX, 2)+pow(self.lineY, 2))
