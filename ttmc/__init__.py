"""init"""
import os
import pygame
from screeninfo import get_monitors

os.chdir(os.path.dirname(__file__))

# Récupérer les dimensions de l'écran
SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height

WINDOW_WIDTH, WINDOW_HEIGHT = SCREEN_WIDTH//2, SCREEN_HEIGHT//2

BOARD_WIDTH, BOARD_HEIGHT = 612, 1029

# Couleurs des cases
RED = (139,0,0)
GREEN = (0,255,127)
BLUE = (0,191,255)
ORANGE = (255,140,0)
PURPLE = (128,0,128)
YELLOW = (255,215,0)
BLACK = (0, 0, 0)

# Autres couleurs
WHITE = (255, 255, 255)

FPS = 60

BACKGROUND = pygame.image.load('Background.jpg')
BOARD = pygame.image.load('Plateau.jpg')
ICON = pygame.image.load('icon.png')
