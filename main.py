import pygame
from pygame.locals import *
import os
import time
import sys
sys.path.insert(0, "./src")

pygame.init()
from constants import *
from functions import *
from buyMenu import BuyMenu

def main():
    scan = "", False
    running = True
    eventHandlers = setHandlers(mainMenuHandlers, fonts)
    buyingMenu = BuyMenu()
    title = fonts["30"].render("Choisissez une action", 1, (0, 0, 0))

    #Functions to call by scanning eventHandlers
    functions = {mainMenuHandlers[0]: buyingMenu.run,
                 mainMenuHandlers[1]: None,
                 mainMenuHandlers[2]: None,
                 mainMenuHandlers[3]: None,
                 mainMenuHandlers[4]: None,
                 mainMenuHandlers[5]: None}

    while running:
        screen.blit(background, (0, 0))
        screen.blit(urlabBanner, (0, 0))
        screen.blit(title, (10, urlabBanner.get_size()[1]+10))
        pygame.draw.line(screen, (125, 125, 125), (10, urlabBanner.get_size()[1]+title.get_size()[1]+10), (250, urlabBanner.get_size()[1]+title.get_size()[1]+10))

        for handler in eventHandlers:
            handler.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                dataBase.save()
                pygame.quit()
                exit()
            scan = fetchScan(event, scan[0])
            if scan[1]:
                for x in range(len(eventHandlers)):
                    if eventHandlers[x].match(scan[0]):
                        print("toCall ", eventHandlers[x].text)
                        functions[eventHandlers[0].text]()
                scan = "", False

        pygame.display.flip()

if __name__ == "__main__":
    main()
