import time
import pygame
from pygame.locals import *

from constants import *

class BasketElement(object):
    def __init__(self, name, price, image="imgs/products/Not_Found.png"):
        self.name = name
        self.price = int(price*100) #Final price, depends on the amount of this product in the basket
        self.basePrice = int(price*100) #Unit price
        self.nb = 1 #Amount of this type of article

        self.image = pygame.image.load(image) #Base image, will be resized

        coef = self.image.get_size()[1]/SIZE_ARTICLE #Coefficient for resizing the image at the desired size
        coef2 = self.image.get_size()[1]/SIZE_LAST_ARTICLE

        self.scaledImage = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef), int(self.image.get_size()[1]/coef))) #Image for an article not at the end of the list
        self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_size()[0]/coef2), int(self.image.get_size()[1]/coef2))) #Image for an article at the end of the list

        self.updateImgs()

    def addOne(self):
        self.nb += 1
        self.price += self.basePrice

        self.updateImgs()

    def removeOne(self):
        self.nb -= 1
        self.price -= self.basePrice

        if self.nb != 0: #If there is no more product of this kind, returns 1 to remove the article from the basket
            self.updateImgs()
            return 0
        return 1

    def updateImgs(self):
        self.nameImage = fonts["20"].render(self.name + " x"+str(self.nb), 1, (0, 0, 0))
        self.priceImage = fonts["20"].render(str(self.price/100)[:4]+"€", 1, (0, 0, 0))

    def draw(self, screen, nb, isLast=False):
        if not isLast:
            screen.blit(self.scaledImage, (312, 90+(nb+1)*50))
            screen.blit(self.nameImage,   (320+self.scaledImage.get_size()[0], 95+(nb+1)*50))
            screen.blit(self.priceImage,  (700-self.priceImage.get_size()[0], 95+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 90+(nb+1)*50), (400, 51)), 1)
        else:
            screen.blit(self.image,      (312, 90+(nb+1)*50))
            screen.blit(self.nameImage,  (320+self.image.get_size()[0], 130+(nb+1)*50))
            screen.blit(self.priceImage, (700-self.priceImage.get_size()[0], 130+(nb+1)*50))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((312, 90+(nb+1)*50), (400, 100)), 1)

#Allows to display alert or information msgs on the screen during a certain amount of time
class AlertMsg(object):
    def __init__(self, msg, length):
        self.message = msg
        self.image = fonts["30"].render(self.message, 1, (250, 100, 100))
        self.timeLeft = length

    def update(self, timeElapsed):
        self.timeLeft -= timeElapsed
        if self.timeLeft <= 0:
            return 1
        return 0

    def draw(self, screen):
        screen.blit(self.image, (SCREEN_X/2 - self.image.get_size()[0]/2, SCREEN_Y - 100))


#The buy menu
class BuyMenu(object):
    def __init__(self):
        self.buying = True
        self.basket = []
        self.handlers = setHandlers(buyMenuHandlers, fonts)
        self.handlersNBC = setHandlers(buyMenuHandlersNBC, fonts)
        self.scan = ("", False)
        self.total = 0
        self.historyArticle = []
        self.alertMsgs = []
        self.mainMenu = True

        self.emptyBasketText = fonts["30"].render("Votre panier est vide !", 1, (250, 120, 120))
        self.title = fonts["30"].render("Menu d'achat", 1, (0, 0, 0))
        self.basketText = fonts["25"].render("Votre panier :", 1, (0, 0, 0))

        self.functions = {buyMenuHandlers[0]: self.removeLast,
                          buyMenuHandlers[1]: self.noBarCode,
                          buyMenuHandlers[2]: self.Stop,
                          buyMenuHandlers[3]: self.EmptyBasket,
                          buyMenuHandlers[4]: None,
                          buyMenuHandlers[5]: self.Finish}

        self.functionsNBC = {buyMenuHandlers[0]: self.addNBC,
                             buyMenuHandlers[1]: self.addNBC,
                             buyMenuHandlers[2]: None,
                             buyMenuHandlers[3]: None,
                             buyMenuHandlers[4]: None,
                             buyMenuHandlers[5]: self.quitNBC}

    def run(self):
        while self.buying:
            startTime = time.time()
            #DRAWING

            screen.blit(background, (0, 0))

            if len(self.basket) == 0: #Alert Empty shopping cart
                screen.blit(self.emptyBasketText, (SCREEN_X/2 - self.emptyBasketText.get_size()[0]/2, 250))
            else: #VOTRE PANIER (souligné)
                screen.blit(self.basketText, (312, 90))
                pygame.draw.line(screen, (0, 0, 0), (312, 90+self.basketText.get_size()[1]), (450, 90+self.basketText.get_size()[1]))
                screen.blit(self.nbArticlesImg, (312, SCREEN_Y-50))
                screen.blit(self.totalImage, (712-self.totalImage.get_size()[0], SCREEN_Y-50))

            for x in range(min(9, len(self.basket))):
                if len(self.basket) >= 9:
                    self.basket[-9+x].draw(screen, x, x+1==9)
                else:
                    self.basket[x].draw(screen, x, x+1==len(self.basket))

            screen.blit(urlabBanner, (0, 0))
            screen.blit(self.title, (10, urlabBanner.get_size()[1]+10))
            pygame.draw.line(screen, (125, 125, 125), (15, urlabBanner.get_size()[1]+self.title.get_size()[1]+10), (1009, urlabBanner.get_size()[1]+self.title.get_size()[1]+10))

            if self.mainMenu:
                for handler in self.handlers:
                    handler.draw(screen)
            else:
                for handler in self.handlersNBC:


            for msg in self.alertMsgs:
                if msg.update(timeElapsed) == 1:
                    msg.draw(screen)
                    del self.alertMsgs[self.alertMsgs.index(msg)]
                    break
                msg.draw(screen)

            #GETTING INPUTS
            for event in pygame.event.get():
                if event.type == QUIT:
                    dataBase.save()
                    pygame.quit()
                    exit()
                self.scan = fetchScan(event, self.scan[0]) #Return the scan and a bool to tell if the scan if completed
                if self.scan[1]: #If the scan is completed
                    self.handleScan()

            #Updates the display
            pygame.display.flip()
            timeElapsed = time.time() - startTime
            startTime = time.time()

    def startNBC(self): #Runs the NoBarCode Menu
        self.mainMenu = False

    def addNBC(product):


    #Gets the input from the scan and calls the function corresponding to the handler or add product in the shopping cart
    def handleScan(self):
        wasAction = False
        #Goes trough handlers to see if one was scanned
        for x in range(len(self.handlers)):
            if self.handlers[x].match(self.scan[0]):
                print("action : ", self.handlers[x].text)
                wasAction = True
                if self.functions[self.handlers[x].text]:
                    self.functions[self.handlers[x].text]() #If the scan is about a linked handler, call the function linked to it
        if not wasAction:
            self.addProduct()

        self.scan = "", False #Reinits the scan

    def addProduct(self):
        #If the scan is about a product
        results = dataBase.fetch(self.scan[0]) #Gives in order the Name, the price and a link to the image
        print(self.scan)
        print(results)
        if results[0] != "":

            self.historyArticle.append(results) #Keep an history to be able to remove last element

            self.total += int(results[1]*100) #Add the price of the product
            alreadyInBasket = False #Try to find if the last scanned product is already in the basket
            for element in self.basket:
                if element.name == results[0]:
                    element.addOne() #If it is, adds one to it
                    alreadyInBasket = True

            if not alreadyInBasket:
                if results[2] == "": #If no image is specified
                    self.basket.append(BasketElement(results[0], results[1]))
                else:
                    self.basket.append(BasketElement(results[0], results[1], results[2]))
            self.updateTotalText()
        else:
            self.alertMsgs.append(AlertMsg("Aucun article trouvé, réessayez", 3))

    #Starts the transaction
    def Finish(self):
        print("Finished")
        #Ask the MONEY
        self.buying = False

    def updateTotalText(self):
        self.nbArticlesImg = fonts["30"].render(str(len(self.historyArticle)) + " Article(s)", 1, (0, 0, 0))
        self.totalImage = fonts["30"].render("Total : "+str(self.total/100)[:4]+"€", 1, (0, 0, 0))

    def EmptyBasket(self):
        self.basket = []
        self.historyArticle = []
        self.total = 0

    def removeLast(self):
        for element in self.basket:
            if element.name == self.historyArticle[-1][0]:
                self.historyArticle = self.historyArticle[:-1]
                self.total -= element.basePrice
                if element.removeOne() == 1:
                    del self.basket[self.basket.index(element)]
                break

        self.updateTotalText()

    #Quits the menu without finishing the order
    def Stop(self):
        self.buying = False
