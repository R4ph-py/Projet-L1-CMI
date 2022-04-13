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


def back_to_main():
    """Back button action"""
    global actual_menu
    actual_menu = 0


def about_btn():
    """About button action"""
    global actual_menu
    actual_menu = 1


def rules_btn():
    """Rules button action"""
    global actual_menu
    actual_menu = 2


def rules2_btn():
    """Rules button action"""
    global actual_menu
    actual_menu = 3


def rules3_btn():
    """Rules button action"""
    global actual_menu
    actual_menu = 4


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
    main_menu_objs.append(Button(220, 310, 200, 100, window).set_text("Partie Locale").set_action(local_btn))
    main_menu_objs.append(Button(500, 310, 200, 100, window).set_text("Partie Multi").set_action(multi_btn))
    main_menu_objs.append(Button(360, 455, 160, 70, window).set_text("Règles").set_action(rules_btn))
    main_menu_objs.append(Button(360, 555, 160, 70, window).set_text("Crédits").set_action(about_btn))
    main_menu_objs.append(Button(620, 655, 120, 70, window).set_text("Quitter").set_action(quit_menu))

    for obj in main_menu_objs:
        obj.set_size(35)

    back_button = Button(85, 45, 120, 50, window).set_size(35).set_text("Retour").set_action(back_to_main)

    about_objs = [Text(WINDOW_WIDTH/2, 280, "Crédit officiel (Image+jeu):", window)]
    about_objs.append(Text(WINDOW_WIDTH/2, 330, "http://tutemetscombien.fr/", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 390, "Adaptation numérique :", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 440, "Raphaël Georges", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 490, "Lucas Panisset", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 540, "Lucas Sigaut", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 590, "Arthur Masson ", window))
    about_objs.append(Text(WINDOW_WIDTH/2, 650, "Adaptation a but scolaire et non lucratif", window))

    for obj in about_objs:
        obj.set_size(28).set_max_pline(0).has_background(1)

    about_objs.append(back_button)

    rules_menu1_objs = [back_button]
    rules_menu1_objs.append(Text(WINDOW_WIDTH/2, 280, "1) Le jeu TTMC :", window).set_size(35).set_max_pline(0).has_background(1))
    rules_menu1_objs.append(Image(WINDOW_WIDTH/2, 370, "Capture 1.jpg", window))
    rules_menu1_objs.append(Text(WINDOW_WIDTH/2, 460, "2) Le but du jeu  :", window).set_size(35).set_max_pline(0).has_background(1))
    rules_menu1_objs.append(Image(WINDOW_WIDTH/2, 560, "Capture 2.jpg", window))
    rules_menu1_objs.append(Button(610, 655, 200, 70, window).set_text("Page Suivante").set_action(rules2_btn).set_size(28))

    rules_menu2_objs = [back_button]
    rules_menu2_objs.append(Button(130, 655, 200, 70, window).set_text("Page Precedente").set_action(rules_btn).set_size(28))
    rules_menu2_objs.append(Text(WINDOW_WIDTH/2, 300, "3) Deroulement du jeu :", window).set_size(35).set_max_pline(0).has_background(1))
    rules_menu2_objs.append(Image(WINDOW_WIDTH/2, 450, "Capture 3.jpg", window))
    rules_menu2_objs.append(Button(610, 655, 200, 70, window).set_text("Page Suivante").set_action(rules3_btn).set_size(28))

    rules_menu3_objs =[back_button]
    rules_menu3_objs.append(Button(130, 655, 200, 70, window).set_text("Page Precedente").set_action(rules2_btn).set_size(28))
    rules_menu3_objs.append(Text(WINDOW_WIDTH/2, 290, "4) Evenement spéciaux et fin du jeu :", window).set_size(35).set_max_pline(0).has_background(1))
    rules_menu3_objs.append(Image(WINDOW_WIDTH/2, 460, "Capture 4.jpg", window))

    objects = [main_menu_objs, about_objs, rules_menu1_objs, rules_menu2_objs, rules_menu3_objs]
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
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for dysp_obj in objects[actual_menu]:
                        if dysp_obj.obj_type() == "button" and dysp_obj.collide_mouse():
                            dysp_obj.action()

        clock.tick(FPS)

actual_menu = 0 # 0 = main menu, 1 = about menu, 2 / 3 / 4 = rules menu

if __name__ == "__main__":
    start()
