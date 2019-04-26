import pygame
from pygame.locals import *

class EventHandler(object):
    def __init__(self, position, edge, code, font=pygame.font.Font("fonts/BebasNeue-Regular.ttf", 20), text=""):
        self.position = position
        self.code = code
        self.edge = edge
        self.font = font
        self.text = text
        self.updateImg()


    def updateImg(self):
        textImg = self.font.render(self.text, 1, (0, 0, 0))
        self.image = pygame.Surface((textImg.get_size()[0]+50, textImg.get_size()[1]))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        if self.edge == "WEST":
            bar = pygame.Surface((40, 10))
            bar.fill((220, 50, 50))

            self.image.blit(textImg, (50, 0))
            self.image.blit(bar, (0, (textImg.get_size()[1]-10)//2))

        elif self.edge == "EAST":
            self.position = self.position[0]-self.image.get_size()[0], self.position[1]
            bar = pygame.Surface((40, 10))
            bar.fill((220, 50, 50))

            self.image.blit(textImg, (0, 0))
            self.image.blit(bar, (textImg.get_size()[0]+10, (textImg.get_size()[1]-10)//2))

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def match(self, code):
        return code == str(self.code)
