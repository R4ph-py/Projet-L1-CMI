"""Gestionnaire de plateau"""
#!/usr/bin/python3
import os
import pygame
import json
from pygame.locals import *
from ttmc import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))

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
    with open("game_status.json", "r", encoding="utf-8") as status_file:
        game_status = json.load(status_file.read())

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_ESCAPE]:
        RUN = False

    for event in pygame.event.get():
        if event.type == QUIT:
            RUN = False

        if event.type == MOUSEBUTTONDOWN:
            pass

    WIN.blit(BOARD, (SCREEN_WIDTH - BOARD.get_width(),0))

    pygame.display.update()
    clock.tick(FPS)
