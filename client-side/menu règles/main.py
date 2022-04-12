"""Menu principal"""
#!/usr/bin/python3
import os
from sre_parse import WHITESPACE
import sys
import platform
import _thread
from turtle import window_height
import pygame
from pygame.locals import *
from ttmc import *

os.chdir(os.path.dirname(__file__))

actual_os = platform.system().lower()

if "windows" in actual_os:
    COMMAND = ""

else:
    COMMAND = "3"

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
        self.btn_color = PURPLE
        self.color_hovered = YELLOW
        self.text_color = YELLOW
        self.text_color_hovered = PURPLE
        self.text = None
        self.action = None

    def set_colors(self, btn_color = None, color_hovered = None, text_color = None, text_color_hovered = None):
        """Setting colors for the button"""
        if btn_color != None:
            self.btn_color = btn_color

        if color_hovered != None:
            self.color_hovered = color_hovered

        if text_color != None:
            self.text_color = text_color

        if text_color_hovered != None:
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
        loc_mouse = pygame.mouse.get_pos()

        if self.x <= loc_mouse[0] <= self.x + self.width and self.y <= loc_mouse[1] <= self.y + self.height:
            pygame.draw.rect(WIN, self.color_hovered, [self.x, self.y, self.width, self.height], border_radius = 30)
            message = buttons_font.render(self.text, True, self.text_color_hovered)

        else:
            pygame.draw.rect(WIN, self.btn_color, [self.x, self.y, self.width, self.height], border_radius = 30)
            message = buttons_font.render(self.text, True, self.text_color)

        WIN.blit(message , (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def obj_type(self):
        """Returns the object type"""
        return "button"

class texte:
    """Text constructor"""
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.back_color = BLACK
        self.text_color = WHITE
        self.text = None
    
    def set_text(self, text):
        """Set text for the button"""
        self.text = text
        return self
    
    def show(self):
        """Show button"""
        pygame.draw.rect(WIN, self.back_color, [self.x, self.y, self.width, self.height], border_radius = 30)
        message = buttons_font.render(self.text, True, self.text_color)
        WIN.blit(message , (self.x - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def obj_type(self):
        """Returns the object type"""
        return "texte"
            
class image:
     """image constructor"""
     def __init__(self, x, y,path):
        self.x = x
        self.y = y
        self.path = path

     def show(self):
        """Show button"""
        image = pygame.image.load(self.path)
        WIN.blit(image , (self.x - image.get_width()/2, self.y  - image.get_height()/2))

     def obj_type(self):
        """Returns the object type"""
        return "image"
    


def local_thread():
    """Thread function for local"""
    os.system(f"python{COMMAND} local_game.py")


def socket_thread():
    """Thread function for socket"""
    os.system(f"python{COMMAND} online_game.py")


def board():
    """Function for drawing the board"""
    os.system(f"python{COMMAND} board.py")

def multi_btn():
    """Multi button action"""
    game_socket = _thread.start_new_thread(socket_thread, ())
    board()


def local_btn():
    """Local button action"""
    game_socket = _thread.start_new_thread(local_thread, ())
    board()


def quit_btn():
    """Quit button action"""
    pygame.quit()
    sys.exit()


def rules_btn():
    """Rules button action"""
    global menus
    menus = 1

def rules2_btn():
    """Rules button action"""
    global menus
    menus = 3
def rules3_btn():
    """Rules button action"""
    global menus
    menus = 4

def about_btn():
    """About button action"""
    global menus
    menus = 2


def back_to_main():
    """Back button action"""
    global menus
    menus = 0


main_menu_objs = []
main_menu_objs.append(Button(120, 260, 200, 100).set_text("Partie Locale").set_action(local_btn))
main_menu_objs.append(Button(400, 260, 200, 100).set_text("Partie Multi").set_action(multi_btn))
main_menu_objs.append(Button(280, 420, 160, 70).set_text("Règles").set_action(rules_btn))
main_menu_objs.append(Button(280, 520, 160, 70).set_text("Crédits").set_action(about_btn))
main_menu_objs.append(Button(560, 620, 120, 70).set_text("Quitter").set_action(quit_btn))

back_button = Button(25, 20, 120, 50).set_text("Retour").set_action(back_to_main)

rules_menu_objs = [back_button]
rules_menu_objs.append(image(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,"Capture.jpg"))
rules_menu_objs.append(image(WINDOW_WIDTH/2,550,"Capture2.jpg"))
rules_menu_objs.append(texte(WINDOW_WIDTH/2, 260, 400, 0).set_text("1)Le jeu TTMC :" ))
rules_menu_objs.append(texte(WINDOW_WIDTH/2, 450, 500, 0).set_text("2)Le but du jeu  :" ))
rules_menu_objs.append(Button(510, 620, 200, 70).set_text("Page Suivante").set_action(rules2_btn))

rules2_menu_objs = [back_button]
rules2_menu_objs.append(Button(30, 620, 200, 70).set_text("Page Precedente ").set_action(rules_btn))
rules2_menu_objs.append(texte(WINDOW_WIDTH/2, 260, 400, 0).set_text("3)Deroulement du jeu :" ))
rules2_menu_objs.append(image(WINDOW_WIDTH/2,450,"Capture3.jpg"))
rules2_menu_objs.append(Button(510, 620, 200, 70).set_text("Page Suivante").set_action(rules3_btn))

rules3_menu_objs =[back_button]
rules3_menu_objs.append(Button(30, 620, 200, 70).set_text("Page Precedente ").set_action(rules2_btn))
rules3_menu_objs.append(texte(WINDOW_WIDTH/2, 260, 400, 0).set_text("3)Evenement spéciaux et fin du jeu :" ))
rules3_menu_objs.append(image(WINDOW_WIDTH/2,450,"Capture4.jpg"))

about_objs = [back_button]
about_objs.append(texte(WINDOW_WIDTH/2, 260, 400, 0).set_text("Crédit officiel (image+jeu):" ))
about_objs.append(texte(WINDOW_WIDTH/2, 290, 400, 0).set_text("http://tutemetscombien.fr/"))
about_objs.append(texte(WINDOW_WIDTH/2, 350, 400, 0).set_text("Adaptation numérique :"))
about_objs.append(texte(WINDOW_WIDTH/2, 380, 400, 0).set_text("Raphaël Georges"))
about_objs.append(texte(WINDOW_WIDTH/2, 470, 400, 0).set_text("Lucas Sigaut"))
about_objs.append(texte(WINDOW_WIDTH/2, 410, 400, 0).set_text("Lucas Panisset"))
about_objs.append(texte(WINDOW_WIDTH/2, 440, 400, 0).set_text("Arthur Masson "))
about_objs.append(texte(WINDOW_WIDTH/2, 570, 400, 0).set_text("Adaptation a but scolaire et non Lucrative"))

menus = 0 # 0 = main menu, 1 = rules menu, 2 = about menu, 3 rules2 menu, 4 rules3 menu

objects = [main_menu_objs, rules_menu_objs, about_objs, rules2_menu_objs, rules3_menu_objs]

while True:
    pygame.display.update()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            for dysp_obj in objects[menus]:
                if dysp_obj.obj_type() == "button":
                    if dysp_obj.x <= mouse[0] <= dysp_obj.x + dysp_obj.width and dysp_obj.y <= mouse[1] <= dysp_obj.y + dysp_obj.height:
                        dysp_obj.action()

    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(MENU_LOGO, (WINDOW_WIDTH//2 - MENU_LOGO.get_width()//2, 10))

    for dysp_obj in objects[menus]:
        dysp_obj.show()

    clock.tick(FPS)
