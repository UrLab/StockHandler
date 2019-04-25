import pygame
from pygame.locals import *

from constants import *

class BasketElement(object):
    def __init__(self, name, image, price):
        self.name = name
        self.price = int(price)

        self.nameImage = fonts["30"].render(self.name, 1, (0, 0, 0))
        self.priceImage = fonts["30"].render(str(self.price), 1, (0, 0, 0))
        self.image = pygame.image.load(image)
        self.scaledImage = pygame.transform.smoothscale()

    def draw(self, screen, nb, isLast=False):
        if not isLast:
            pygame.draw.rectangle(screen, (0, 0, 0), pygame.Rect((362, 100+x*50), (300, 50)))

class BuyMenu(object):
    def __init__(self):
        self.buying = True
        self.basket = []
        self.handlers = setHandlers(buyMenuHandlers, fonts)
        self.scan = ("", False)

        self.functions = {buyMenuHandlers[0]: self.removeLast,
                          buyMenuHandlers[1]: None,
                          buyMenuHandlers[2]: self.Stop,
                          buyMenuHandlers[3]: self.EmptyBasket,
                          buyMenuHandlers[4]: None,
                          buyMenuHandlers[5]: self.Finish}

    def run(self):
        while self.buying:
            screen.blit(background, (0, 0))
            screen.blit(urlabBanner, (0, 0))

            for handler in self.handlers:
                handler.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    dataBase.save()
                    pygame.quit()
                    exit()
                self.scan = fetchScan(event, self.scan[0])
                if self.scan[1]:
                    print(self.scan)
                    print(dataBase.fetch(self.scan))
                    for x in range(len(self.handlers)):
                        if self.handlers[x].match(self.scan[0]):
                            print("action : ", self.handlers[x].text)
                            self.functions[self.handlers[x].text]()
                    self.scan = "", False

            pygame.display.flip()

    def Finish(self):
        print("Finished")
        #Ask the MONEY
        self.buying = False

    def EmptyBasket(self):
        self.basket = []

    def removeLast(self):
        self.basket = self.basket[:-1]

    def Stop(self):
        self.buying = False
