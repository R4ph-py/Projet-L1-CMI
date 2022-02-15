"""Menu principal"""
import os
import sys
import _thread
import pygame
from pygame.locals import *
from ttmc import *

os.chdir(os.path.dirname(__file__))

pygame.init()

clock = pygame.time.Clock()

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

WIN.fill(WHITE)
pygame.display.set_caption("Menu principal")
pygame.display.set_icon(ICON)

buttons_font = pygame.font.SysFont('Corbel', 35)

class Button:
    """Button constructor"""
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.btn_color = WHITE
        self.color_hovered = YELLOW
        self.text_color = BLACK
        self.text = None
        self.action = None

    def set_colors(self, btn_color = None, color_hovered = None, text_color = None):
        """Setting colors for the button"""
        self.btn_color = btn_color
        self.color_hovered = color_hovered
        self.text_color = text_color
        return self

    def set_text(self, text):
        """Set text for the button"""
        self.text = text
        return self

    def set_action(self, action):
        """Set action of the button"""
        self.action = action
        return self

    def show(self):
        """Show button"""
        loc_mouse = pygame.mouse.get_pos()

        if self.x <= loc_mouse[0] <= self.x + self.width and self.y <= loc_mouse[1] <= self.y + self.height:
            pygame.draw.rect(WIN, self.color_hovered, [self.x, self.y, self.width, self.height], border_radius = 30)

        else:
            pygame.draw.rect(WIN, self.btn_color, [self.x, self.y, self.width, self.height], border_radius = 30)

        message = buttons_font.render(self.text, True , self.text_color)
        WIN.blit(message , (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def obj_type(self):
        """Returns the object type"""
        return "button"


def socket_thread():
    """Thread function for socket"""
    os.system("python3 websocket.py")

def multi_btn():
    """Multi button action"""
    game_socket = _thread.start_new_thread(socket_thread)
    launch_btn()

def launch_btn():
    """Launch button action"""
    os.system("python3 game.py")

def quit_btn():
    """Quit button action"""
    pygame.quit()
    sys.exit()

def rules_btn():
    """Rules button action"""
    global menus
    menus = {0: False, 1: True, 2: False}

def about_btn():
    """About button action"""
    global menus
    menus = {0: False, 1: False, 2: True}

def back_to_main():
    """Back button action"""
    global menus
    menus = {0: True, 1: False, 2: False}

main_menu_objs = []
main_menu_objs.append(Button(120, 260, 200, 100).set_text("Partie Locale").set_action(launch_btn))
main_menu_objs.append(Button(400, 260, 200, 100).set_text("Partie Multi").set_action(multi_btn))
main_menu_objs.append(Button(280, 420, 160, 70).set_text("Règles").set_action(rules_btn))
main_menu_objs.append(Button(280, 520, 160, 70).set_text("Crédits").set_action(about_btn))
main_menu_objs.append(Button(560, 620, 120, 70).set_text("Quitter").set_action(quit_btn))

back_button = Button(25, 20, 120, 50).set_text("Retour").set_action(back_to_main)

rules_menu_objs = [back_button]

about_objs = [back_button]

menus = {0: True, 1: False, 2: False} # 0 = main menu, 1 = rules menu, 2 = about menu

objects = [main_menu_objs, rules_menu_objs, about_objs]

while True:
    pygame.display.update()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for menu, value in menus.items():
                if value:
                    for dysp_obj in objects[menu]:
                        if dysp_obj.obj_type() == "button":
                            if dysp_obj.x <= mouse[0] <= dysp_obj.x + dysp_obj.width and dysp_obj.y <= mouse[1] <= dysp_obj.y + dysp_obj.height:
                                dysp_obj.action()

    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(MENU_LOGO, (WINDOW_WIDTH//2 - MENU_LOGO.get_width()//2, 10))

    for menu, value in menus.items():
        if value:
            for dysp_obj in objects[menu]:
                dysp_obj.show()

    clock.tick(FPS)
