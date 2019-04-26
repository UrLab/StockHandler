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
        coef = self.image.get_size()[1]/SIZE_ARTICLE
        coef2 = self.image.get_size()[1]/SIZE_LAST_ARTICLE
        self.scaledImage = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef), int(self.image.get_size()[1]/coef)))
        self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef2), int(self.image.get_size()[1]/coef2)))

    def draw(self, screen, nb, isLast=False):
        if not isLast:
            screen.blit(self.scaledImage, (312, 80+(nb+1)*50))
            screen.blit(self.nameImage,   (320+self.scaledImage.get_size()[0], 85+(nb+1)*50))
            screen.blit(self.priceImage,  (700-self.priceImage.get_size()[0], 85+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 80+(nb+1)*50), (400, 51)), 1)
        else:
            screen.blit(self.image,      (312, 80+(nb+1)*50))
            screen.blit(self.nameImage,  (320+self.image.get_size()[0], 120+(nb+1)*50))
            screen.blit(self.priceImage, (700-self.priceImage.get_size()[0], 120+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 80+(nb+1)*50), (400, 100)), 1)

class BuyMenu(object):
    def __init__(self):
        self.buying = True
        self.basket = []
        self.handlers = setHandlers(buyMenuHandlers, fonts)
        self.scan = ("", False)
        self.total = 0

        self.emptyBasketText = fonts["30"].render("Votre panier est vide !", 1, (250, 120, 120))
        self.title = fonts["30"].render("Menu d'achat", 1, (0, 0, 0))
        self.basketText = fonts["25"].render("Votre panier :", 1, (0, 0, 0))

        self.functions = {buyMenuHandlers[0]: self.removeLast,
                          buyMenuHandlers[1]: None,
                          buyMenuHandlers[2]: self.Stop,
                          buyMenuHandlers[3]: self.EmptyBasket,
                          buyMenuHandlers[4]: None,
                          buyMenuHandlers[5]: self.Finish}

    def run(self):
        while self.buying:
            #DRAWING

            screen.blit(background, (0, 0))

            if len(self.basket) == 0:
                #Alert Empty shopping cart
                screen.blit(self.emptyBasketText, (SCREEN_X/2 - self.emptyBasketText.get_size()[0]/2, 250))
            else:
                #VOTRE PANIER (souligné)
                screen.blit(self.basketText, (312, 90))
                pygame.draw.line(screen, (0, 0, 0), (312, 90+self.basketText.get_size()[1]), (450, 90+self.basketText.get_size()[1]))
            for x in range(len(self.basket)):
                self.basket[x].draw(screen, x, x+1==len(self.basket))

            screen.blit(urlabBanner, (0, 0))
            screen.blit(self.title, (10, urlabBanner.get_size()[1]+10))
            pygame.draw.line(screen, (125, 125, 125), (10, urlabBanner.get_size()[1]+self.title.get_size()[1]+10), (250, urlabBanner.get_size()[1]+self.title.get_size()[1]+10))

            for handler in self.handlers:
                handler.draw(screen)

            #GETTING INPUTS
            for event in pygame.event.get():
                if event.type == QUIT:
                    dataBase.save()
                    pygame.quit()
                    exit()
                self.scan = fetchScan(event, self.scan[0]) #Return the scan and a bool to tell if the scan if completed
                if self.scan[1]: #If the scan is completed
                    wasAction = False
                    #Goes trough handlers to see if one was scanned
                    for x in range(len(self.handlers)):
                        if self.handlers[x].match(self.scan[0]):
                            print("action : ", self.handlers[x].text)
                            wasAction = True
                            self.functions[self.handlers[x].text]() #If the scan is about a handler, call the function linked to it
                    #If the scan is about a product
                    if not wasAction:
                        results = dataBase.fetch(self.scan[0]) #Gives in order the Name, the price and a link to the image
                        print(self.scan)
                        print(results)
                        if results[0] != "":
                            self.total += results[1] #Add the price of the product
                            self.updateTotalText()

                            if results[2] == "": #If no image is specified
                                self.basket.append(BasketElement(results[0], results[1]))
                            else:
                                self.basket.append(BasketElement(results[0], results[1], results[2]))
                    self.scan = "", False #Reinits the scan

            #Updates the display
            pygame.display.flip()

    #Starts the transaction
    def Finish(self):
        print("Finished")
        #Ask the MONEY
        self.buying = False

    def updateTotalText(self):
        self.totalImage = fonts["30"].render(str(self.total), 1, (0, 0, 0))

    def EmptyBasket(self):
        self.basket = []

    def removeLast(self):
        self.total -= self.basket[-1].price #Remove the price of the last product from the total
        self.updateTotalText() #Updates the image
        self.basket = self.basket[:-1]

    #Quits the menu without finishing the order
    def Stop(self):
        self.buying = False
