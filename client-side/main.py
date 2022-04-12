"""Menu principal"""
#!/usr/bin/python3
import os
import sys
import platform
import _thread
import pygame
from pygame.locals import *
from ttmc import *

actual_os = platform.system().lower()
actual_path = os.path.dirname(__file__)

if "windows" in actual_os:
    COMMAND = ""

else:
    COMMAND = "3"

def launch_board(is_online):
    """Launch board"""
    os.system(f"python{COMMAND} \"{actual_path}/board.py\" {is_online}")

def multi_btn():
    """Multi button action"""
    board_thread = _thread.start_new_thread(launch_board, (1,))


def local_btn():
    """Local button action"""
    board_thread = _thread.start_new_thread(launch_board, (0,))


def quit_menu():
    """Quit button action"""
    pygame.quit()
    sys.exit()


def rules_btn():
    """Rules button action"""
    global actual_menu
    actual_menu = 1


def about_btn():
    """About button action"""
    global actual_menu
    actual_menu = 2


def back_to_main():
    """Back button action"""
    global actual_menu
    actual_menu = 0


def start():
    """Démarrer le menu"""
    global actual_menu
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill(WHITE)
    pygame.display.set_caption("Menu principal")
    pygame.display.set_icon(ICON)

    clock = pygame.time.Clock()

    bg = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

    main_menu_objs = []
    main_menu_objs.append(Button(220, 310, 200, 100, window).set_size(35).set_text("Partie Locale").set_action(local_btn))
    main_menu_objs.append(Button(500, 310, 200, 100, window).set_size(35).set_text("Partie Multi").set_action(multi_btn))
    main_menu_objs.append(Button(360, 455, 160, 70, window).set_size(35).set_text("Règles").set_action(rules_btn))
    main_menu_objs.append(Button(360, 555, 160, 70, window).set_size(35).set_text("Crédits").set_action(about_btn))
    main_menu_objs.append(Button(620, 655, 120, 70, window).set_size(35).set_text("Quitter").set_action(quit_menu))

    back_button = Button(85, 45, 120, 50, window).set_size(35).set_text("Retour").set_action(back_to_main)

    rules_menu_objs = [back_button]

    about_objs = [back_button]

    objects = [main_menu_objs, rules_menu_objs, about_objs]
    stay = 1
    while stay:
        pygame.display.update()

        window.blit(bg, (0, 0))
        window.blit(MENU_LOGO, (WINDOW_WIDTH//2 - MENU_LOGO.get_width()//2, 10))

        for dysp_obj in objects[actual_menu]:
            dysp_obj.show()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                stay = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for dysp_obj in objects[actual_menu]:
                        if dysp_obj.obj_type() == "button" and dysp_obj.collide_mouse():
                            dysp_obj.action()

        clock.tick(FPS)

actual_menu = 0 # 0 = main menu, 1 = rules menu, 2 = about menu

if __name__ == "__main__":
    start()
