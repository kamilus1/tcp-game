from random import randint
import pygame
from boxes import Box
from math import pow
class GenerateWorld:
    def __init__(self,  width=None, height=None, box_quantity=None, boxes_x=None, boxes_y=None):
        if not width:
            width = randint(5000, 10000)
        self.width = width
        if not height:
            height = randint(5000, 10000)
        self.height = height
        if not box_quantity:
            box_quantity = randint(40, 100)
        self.Box = Box()
        self.boxes_x = boxes_x
        self.boxes_y = boxes_y
        self.boxes = box_quantity
    def __int__(self):
        return self.width, self.height, self.boxes
    def drawWorld(self,screen, x, y, color):
        pygame.draw.rect(screen, color, (x, y, self.width, self.height))
    def drawBoxes(self, player_x, player_y, player_x1, player_y1, screen, boxes_status, hp, dmg, speed, mana):
        for i in range(0, self.boxes):
            if boxes_status[i] == 0:
                pos_x = self.boxes_x[i] - player_x
                pos_y = self.boxes_y[i] - player_y
                pos_x += player_x1
                pos_y += player_y1
                self.Box.showBox(screen, pos_x, pos_y)
                if player_x > pos_x and player_x < pos_x + 50:
                    if player_y > pos_y and player_y < pos_y + 50:
                        boxes_status[i] = 1
                        print("elo")

        return boxes_status