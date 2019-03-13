import pygame
import math


class Bullet:
    def __init__(self, screen):
        self.image = pygame.image.load("harnas1.png")
        self.screen = screen
        self.speed_x = 0
        self.speed_y = 0
        self.control = 0
    def display(self, x, y, start_x, start_y, shot):
        self.x = x
        self.y = y
        self.screen.blit(self.image, (self.x, self.y))
        if pygame.mouse.get_pressed()[0]:
            self.x = start_x
            self.y = start_y
            self.pitagores()
            self.rotate()
            if pygame.mouse.get_rel()[0]:
                self.shot()
                self.control = 1
                shot = True
        if shot:
            self.x += self.speed_x
            self.y += self.speed_y
        return self.x, self.y, shot
    def pitagores(self):
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.line_x = self.mouse_x - (self.x + 25)
        self.line_x2 = self.line_x * self.line_x
        self.line_y = self.mouse_y - (25 + self.y)
        self.line_y2 = self.line_y * self.line_y
    def shot(self):
        self.speed_y = self.line_y
        self.speed_y /= math.sqrt(self.line_x2+self.line_y2)
        self.speed_x = self.line_x
        self.speed_x /= math.sqrt(self.line_x2 + self.line_y2)
        self.speed_x *= 15
        self.speed_y *= 15
    def rotate(self):
            self.image = pygame.image.load("harnas1.png")
            x_line = self.line_x
            y_line = self.line_y
            if x_line < 0:
                x_line *= -1
                y_line /= math.sqrt(self.line_x2+self.line_y2)
                angle = math.degrees(math.sin(y_line))
                if angle<0:
                    angle +=2
                else:
                    angle -=2
                self.image = pygame.transform.rotate(self.image, 90+2*(angle))
            else:
                x_line *= -1
                y_line /= math.sqrt(self.line_x2 + self.line_y2)
                angle = math.degrees(math.sin(y_line))
                if angle<0:
                    angle +=2
                else:
                    angle -=2
                self.image = pygame.transform.rotate(self.image, 270-2*angle)