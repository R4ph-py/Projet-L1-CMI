"""Gestionnaire de plateau"""
import os
from ttmc import *
import pygame
from pygame.locals import *

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"

pygame.init()

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
BOARD = pygame.transform.scale(BOARD, (SCREEN_HEIGHT // BOARD_HEIGHT * BOARD_WIDTH, SCREEN_HEIGHT))

WIN.fill(WHITE)
pygame.display.set_caption('TTMC')
pygame.display.set_icon(ICON)

RUN = True
clock = pygame.time.Clock()

while RUN:
    pygame.display.update()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_ESCAPE]:
        RUN = False

    for event in pygame.event.get():
        if event.type == QUIT:
            RUN = False

        if event.type == MOUSEBUTTONDOWN:
            pass

    WIN.blit(BOARD, (SCREEN_WIDTH - BOARD.get_width(),0))

    clock.tick(FPS)
