"""Menu principal"""
import os
import sys
import _thread
from ttmc import *
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

WIN.fill(WHITE)
pygame.display.set_caption("Menu principal")
pygame.display.set_icon(ICON)

smallfont = pygame.font.SysFont('Corbel', 35)

quit_message = smallfont.render('Quitter', True , BLACK)
quit_btn_x = WINDOW_WIDTH*2//5
quit_btn_y = WINDOW_HEIGHT*3//4
quit_btn_w = WINDOW_WIDTH*3//5 - quit_btn_x
quit_btn_h = WINDOW_HEIGHT*9//10 - quit_btn_y

while True:
    pygame.display.update()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if quit_btn_x <= mouse[0] <= quit_btn_x + quit_btn_w and quit_btn_y <= mouse[1] <= quit_btn_y + quit_btn_h:
                pygame.quit()
                sys.exit()

    WIN.blit(BACKGROUND, (0,0))

    if quit_btn_x <= mouse[0] <= quit_btn_x + quit_btn_w and quit_btn_y <= mouse[1] <= quit_btn_y + quit_btn_h:
        pygame.draw.rect(WIN, YELLOW, [quit_btn_x, quit_btn_y, quit_btn_w, quit_btn_h])

    else:
        pygame.draw.rect(WIN, WHITE, [quit_btn_x, quit_btn_y, quit_btn_w, quit_btn_h])

    WIN.blit(quit_message , (quit_btn_x + quit_btn_w//2 - quit_message.get_width()//2, quit_btn_y + quit_btn_h//2 - quit_message.get_height()//2))

    clock.tick(FPS)
