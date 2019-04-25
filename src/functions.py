import pygame
from pygame.locals import *
from eventHandler import EventHandler

#Defines the different options in the current menu
def setHandlers(names, fonts):
    eventHandlers = []
    for x in [0, 1024]:
        for y in [245, 445, 645]:
            if x == 0:
                eventHandlers.append(EventHandler((x, y), "WEST", ((y-45)//200)-1, font=fonts["30"], text=names[((y-45)//200)-1]))
            else:
                eventHandlers.append(EventHandler((x, y), "EAST", 3+((y-45)//200)-1, font=fonts["30"], text=names[3+(((y-45)//200)-1)]))
    return eventHandlers

#Get the scan result
def fetchScan(event, text):
    if event.type == KEYDOWN:
        if event.key == K_RETURN:
            final = text
            return final, True
        elif event.key == K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode
    return text, False


#BANNER
def CreateBanner(fonts, SCREEN_X):
    title = fonts["50"].render("UrLab's stock handler", 1, (0, 0, 0))
    urlabImg = pygame.image.load("imgs/UrLabBan.png")
    coef = urlabImg.get_size()[1]/title.get_size()[1]
    urlabImg = pygame.transform.smoothscale(urlabImg, (int(urlabImg.get_size()[0]/coef), int(urlabImg.get_size()[1]/coef)))

    banner = pygame.Surface((1024, 16+urlabImg.get_size()[1]))
    banner.fill((255, 255, 255))
    banner.blit(title, (10, 8))
    banner.blit(urlabImg, (SCREEN_X - 10-urlabImg.get_size()[0], 8))
    pygame.draw.line(banner, (50, 50, 50), (0, 15+urlabImg.get_size()[1]), (SCREEN_X, 15+urlabImg.get_size()[1]))

    return banner
