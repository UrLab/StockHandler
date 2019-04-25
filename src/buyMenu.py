import pygame
from pygame.locals import *

from constants import *

class BasketElement(object):
    def __init__(self, name, price, image="imgs/products/Not_Found.png"):
        self.name = name
        self.price = float(price)

        self.nameImage = fonts["20"].render(self.name, 1, (0, 0, 0))
        self.priceImage = fonts["20"].render(str(self.price)+"€", 1, (0, 0, 0))
        self.image = pygame.image.load(image)
        coef = self.image.get_size()[1]/50
        coef2 = self.image.get_size()[1]/120
        self.scaledImage = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef), int(self.image.get_size()[1]/coef)))
        self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef2), int(self.image.get_size()[1]/coef2)))

    def draw(self, screen, nb, isLast=False):
        if not isLast:
            screen.blit(self.scaledImage, (312, 75+(nb+1)*50))
            screen.blit(self.nameImage,   (312+self.scaledImage.get_size()[0], 80+(nb+1)*50))
            screen.blit(self.priceImage,  (700-self.priceImage.get_size()[0], 80+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 75+(nb+1)*50), (400, 51)), 1)
        else:
            screen.blit(self.image,      (312, 75+(nb+1)*50))
            screen.blit(self.nameImage,  (312+self.image.get_size()[0], 95+(nb+1)*50))
            screen.blit(self.priceImage, (700-self.priceImage.get_size()[0], 95+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 75+(nb+1)*50), (400, 120)), 1)

class BuyMenu(object):
    def __init__(self):
        self.buying = True
        self.basket = []
        self.handlers = setHandlers(buyMenuHandlers, fonts)
        self.scan = ("", False)

        self.emptyBasketText = fonts["30"].render("Panier vide !", 1, (250, 120, 120))

        self.functions = {buyMenuHandlers[0]: self.removeLast,
                          buyMenuHandlers[1]: None,
                          buyMenuHandlers[2]: self.Stop,
                          buyMenuHandlers[3]: self.EmptyBasket,
                          buyMenuHandlers[4]: None,
                          buyMenuHandlers[5]: self.Finish}

    def run(self):
        while self.buying:
            screen.blit(background, (0, 0))

            if len(self.basket) == 0:
                screen.blit(self.emptyBasketText, (SCREEN_X/2 - self.emptyBasketText.get_size()[0]/2, 250))
            for x in range(len(self.basket)):
                self.basket[x].draw(screen, x, x+1==len(self.basket))

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
                    wasAction = False
                    for x in range(len(self.handlers)):
                        if self.handlers[x].match(self.scan[0]):
                            print("action : ", self.handlers[x].text)
                            wasAction = True
                            self.functions[self.handlers[x].text]()
                    if not wasAction:
                        results = dataBase.fetch(self.scan[0])
                        print(self.scan)
                        print(results)
                        if results[0] != "":
                            print("Appening to the basket")
                            if results[2] == "":
                                self.basket.append(BasketElement(results[0], results[1]))
                            else:
                                self.basket.append(BasketElement(results[0], results[1], results[2]))
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
