import pygame

class Map(object):
    def __init__(self, screen, width, height, boxes_x, boxes_y, enemies_x, enemies_y):
        self.screen = screen
        self.scale_x = 800 / width
        self.scale_y = 600 / height
        self.boxes_amount = len(boxes_x)
        self.boxes_x = boxes_x
        self.boxes_y = boxes_y
        self.enemies_amount = len(enemies_x)
        self.enemies_x = enemies_x
        self.enemies_y = enemies_y
        self.x = 112
        self.y = 50
        self.red = (200, 50, 50)
        self.blue = (60, 90, 220)
        self.green = (50, 150, 10)
        self.black = (0, 0, 0)
        self.yellow = 	(255, 215, 0)
    def display(self, your_x, your_y):
        pygame.draw.rect(self.screen, self.black, (self.x-10, self.y-10, 820, 620))
        pygame.draw.rect(self.screen, self.green, (self.x, self.y, 800, 600))
        for i in range(0, self.boxes_amount):
            pygame.draw.rect(self.screen, self.blue, (self.x+(self.boxes_x[i]*self.scale_x), self.y+(self.boxes_y[i]*self.scale_y), 5, 5))

        pygame.draw.rect(self.screen, self.yellow, (self.x+your_x*self.scale_x, self.y+your_y*self.scale_y, 5, 5))