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
# MENU_LOGO = pygame.transform.scale(MENU_LOGO, (WINDOW_WIDTH, WINDOW_HEIGHT//8))

WIN.fill(WHITE)
pygame.display.set_caption("Menu principal")
pygame.display.set_icon(ICON)

buttons_font = pygame.font.SysFont('Corbel', WINDOW_WIDTH//25)
main_text_font = pygame.font.SysFont('Landman', WINDOW_WIDTH//10)

class Text:
    """Text constructor"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.text_color = BLACK
        self.text = None
        self.action = None

    def set_colors(self, text_color = None):
        """Setting colors for the button"""
        self.text_color = text_color
        return self

    def set_text(self, text):
        """Set text for the button"""
        self.text = text
        return self

    def show(self):
        """Show button"""

        message = main_text_font.render(self.text, True , self.text_color)
        WIN.blit(message , (self.x - message.get_width()/2, self.y - message.get_height()/2))

    def obj_type(self):
        """Returns the object type"""
        return "text"


class Button:
    """Button constructor"""
    def __init__(self, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
            pygame.draw.rect(WIN, self.color_hovered, [self.x, self.y, self.width, self.height])

        else:
            pygame.draw.rect(WIN, self.btn_color, [self.x, self.y, self.width, self.height])

        message = buttons_font.render(self.text, True , self.text_color)
        WIN.blit(message , (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def obj_type(self):
        """Returns the object type"""
        return "button"

btn_h = WINDOW_HEIGHT//5
btn_w = WINDOW_WIDTH//5
mid_left_btn_x = WINDOW_WIDTH//3 - btn_w//2
mid_btn_x = WINDOW_WIDTH//2 - btn_w//2
mid_right_btn_x = WINDOW_WIDTH*2//3 - btn_w//2
top_btn_y = WINDOW_HEIGHT//25
center1_btn_y = top_btn_y*2 + btn_h
center2_btn_y = top_btn_y*3 + btn_h*2
bottom_btn_y = top_btn_y*4 + btn_h*3

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

main_menu_objs = [Button(btn_w, btn_h, mid_left_btn_x, top_btn_y).set_text("Multiplayer").set_action(multi_btn)]
main_menu_objs.append(Button(btn_w, btn_h, mid_right_btn_x, top_btn_y).set_text("Local").set_action(launch_btn))
main_menu_objs.append(Button(btn_w, btn_h, mid_btn_x, center1_btn_y).set_text("Règles").set_action(rules_btn))
main_menu_objs.append(Button(btn_w, btn_h, mid_btn_x, center2_btn_y).set_text("Crédits").set_action(about_btn))
main_menu_objs.append(Button(btn_w, btn_h, mid_btn_x, bottom_btn_y).set_text("Quitter").set_action(quit_btn))
main_menu_objs.append(Text(200, 200).set_text(""))

back_button = Button(btn_w, btn_h, mid_left_btn_x, top_btn_y).set_text("Retour").set_action(back_to_main)

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

    WIN.blit(BACKGROUND, (0,0))

    for menu, value in menus.items():
        if value:
            for dysp_obj in objects[menu]:
                dysp_obj.show()

    clock.tick(FPS)
