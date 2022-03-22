"""Menu principal"""
#!/usr/bin/python3
import os
import sys
import platform
import _thread
import pygame
from pygame.locals import *
import ttmc
from ttmc import *

class Text:
    """Text constructor"""
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.font = "Corbel"
        self.size = 20
        self.text_color = BLACK

    def set_colors(self, text_color):
        """Setting color for the text"""
        self.text_color = text_color
        return self

    def set_text(self, text):
        """Set the text"""
        self.text = text
        return self

    def set_font(self, font):
        """Set font for the text"""
        self.font = font
        return self

    def set_size(self, size):
        """Set font size for the text"""
        self.size = size
        return self

    def show(self):
        """Show text"""
        text_font = pygame.font.SysFont(self.font, self.size)
        message = text_font.render(self.text, True, self.text_color)

        WIN.blit(message, (self.x, self.y))

    def obj_type(self):
        """Returns the object type"""
        return "text"

class Button:
    """Button constructor"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.btn_color = PURPLE
        self.text_color = YELLOW
        self.btn_color_hovered = YELLOW
        self.text_color_hovered = PURPLE
        self.text = ""
        self.font = "Corbel"
        self.action = None
        self.rect = pygame.Rect(x, y, width, height)

    def set_colors(self, btn_color = None, btn_color_hovered = None, text_color = None, text_color_hovered = None):
        """Setting colors for the button"""
        if btn_color is not None:
            self.btn_color = btn_color

        if btn_color_hovered is not None:
            self.btn_color_hovered = btn_color_hovered

        if text_color is not None:
            self.text_color = text_color

        if text_color_hovered is not None:
            self.text_color_hovered = text_color_hovered

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
        button_font = pygame.font.SysFont(self.font, 35)

        if self.collide_mouse():
            pygame.draw.rect(WIN, self.btn_color_hovered, self.rect, border_radius = 30)
            message = button_font.render(self.text, True, self.text_color_hovered)

        else:
            pygame.draw.rect(WIN, self.btn_color, self.rect, border_radius = 30)
            message = button_font.render(self.text, True, self.text_color)

        WIN.blit(message, (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def collide_mouse(self):
        """Check if mouse is over the button"""
        loc_mouse = pygame.mouse.get_pos()
        return 1 if self.rect.collidepoint(loc_mouse) else 0

    def obj_type(self):
        """Returns the object type"""
        return "button"


def local_thread():
    """Thread function for local"""
    ttmc.local_game.start()


def socket_thread():
    """Thread function for socket"""
    ttmc.online_game.start()


def board():
    """Function for drawing the board"""
    ttmc.board.start()


def multi_btn():
    """Multi button action"""
    game_socket = _thread.start_new_thread(socket_thread, ())
    board()


def local_btn():
    """Local button action"""
    game_socket = _thread.start_new_thread(local_thread, ())
    board()


def quit_menu():
    """Quit button action"""
    pygame.quit()
    sys.exit()


def rules_btn():
    """Rules button action"""
    global ACTUAL_MENU
    ACTUAL_MENU = 1


def about_btn():
    """About button action"""
    global ACTUAL_MENU
    ACTUAL_MENU = 2


def back_to_main():
    """Back button action"""
    global ACTUAL_MENU
    ACTUAL_MENU = 0


def start():
    """Démarrer le menu"""
    stay = 1
    while stay:
        pygame.display.update()

        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(MENU_LOGO, (WINDOW_WIDTH//2 - MENU_LOGO.get_width()//2, 10))

        for dysp_obj in objects[ACTUAL_MENU]:
            dysp_obj.show()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                stay = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for dysp_obj in objects[ACTUAL_MENU]:
                        if dysp_obj.obj_type() == "button":
                            if dysp_obj.collide_mouse():
                                dysp_obj.action()

        clock.tick(FPS)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
actual_os = platform.system().lower()

if "windows" in actual_os:
    COMMAND = ""

else:
    COMMAND = "3"

pygame.init()

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WIN.fill(WHITE)
pygame.display.set_caption("Menu principal")
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

main_menu_objs = []
main_menu_objs.append(Button(120, 260, 200, 100).set_text("Partie Locale").set_action(local_btn))
main_menu_objs.append(Button(400, 260, 200, 100).set_text("Partie Multi").set_action(multi_btn))
main_menu_objs.append(Button(280, 420, 160, 70).set_text("Règles").set_action(rules_btn))
main_menu_objs.append(Button(280, 520, 160, 70).set_text("Crédits").set_action(about_btn))
main_menu_objs.append(Button(560, 620, 120, 70).set_text("Quitter").set_action(quit_menu))

back_button = Button(25, 20, 120, 50).set_text("Retour").set_action(back_to_main)

rules_menu_objs = [back_button]

about_objs = [back_button]

ACTUAL_MENU = 0 # 0 = main menu, 1 = rules menu, 2 = about menu

objects = [main_menu_objs, rules_menu_objs, about_objs]

if __name__ == "__main__":
    start()
