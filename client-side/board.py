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

WIN.fill(WHITE)
pygame.display.set_caption('TTMC')
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

BG = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

STATE = 0 # 0 = config players, 1 = game itself

objects = []

def start():
    """Démarrer le plateau"""
    stay = 1
    while stay:
        pygame.display.update()

        WIN.blit(BG, (0, 0))
        WIN.blit(BOARD_FAT, (SCREEN_WIDTH // 2 - BOARD_FAT.get_width() // 2, SCREEN_HEIGHT - BOARD_FAT.get_height()))

        # for dysp_obj in objects[STATE]:
        #     dysp_obj.show()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            stay = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                stay = 0

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         for dysp_obj in objects[STATE]:
            #             if dysp_obj.obj_type() == "button":
            #                 if dysp_obj.collide_mouse():
            #                     dysp_obj.action()

        clock.tick(FPS)

if __name__ == '__main__':
    start()
