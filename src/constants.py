import random
import pygame
from pygame.locals import *


from functions import *
from db import *

#SCREEN
SCREEN_X = 1024
SCREEN_Y = 768
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

#FONTS
if random.random() < 0.33:
    fontToLoad = 'fonts/comic-sans-ms.ttf'
else:
    fontToLoad = 'fonts/BebasNeue-Regular.ttf'

fonts = {}
for x in [14, 20, 25, 30, 35, 50, 75, 100]:
    fonts[str(x)] = pygame.font.Font(fontToLoad, x)

#IMAGES MADE BY THE COMPUTER
urlabBanner = CreateBanner(fonts, SCREEN_X)
background = pygame.image.load("imgs/background.png")

#HANDLERS
mainMenuHandlers = ["Acheter", "Remplir", "Stock", "BDD", "", "Mon solde"]
buyMenuHandlers  = ["Annuler dernier", "", "Retour", "Vider", "", "Terminer"]

#DATABASE
dataBase = DataBase('data/db.json')

#GLOBAL VARS
SIZE_ARTICLE = 50
SIZE_LAST_ARTICLE = 100
