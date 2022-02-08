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

font = pygame.font.SysFont('Corbel', WINDOW_WIDTH//25)

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

        message = font.render(self.text, True , self.text_color)
        WIN.blit(message , (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

btn_h = WINDOW_HEIGHT/5
btn_w = (16/9)*btn_h
left_btn_x = WINDOW_WIDTH/4 - btn_w/2
mid_btn_x = WINDOW_WIDTH/2 - btn_w/2
right_btn_x = WINDOW_WIDTH*3/4 - btn_w/2

top_btn_y = WINDOW_HEIGHT/16

center_btn_y = WINDOW_HEIGHT/4 + WINDOW_HEIGHT/8

bottom_btn_y = WINDOW_HEIGHT/2 + WINDOW_HEIGHT*3/16

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

def rules_btn():
    """Rules button action"""
    global MAIN_MENU
    global RULES_MENU
    global ABOUT_MENU
    MAIN_MENU = False
    RULES_MENU = True
    ABOUT_MENU = False

def quit_btn():
    """Quit button action"""
    pygame.quit()
    sys.exit()

def about_btn():
    """About button action"""
    global MAIN_MENU
    global RULES_MENU
    global ABOUT_MENU
    MAIN_MENU = False
    RULES_MENU = False
    ABOUT_MENU = True

main_buttons = []
main_buttons.append(Button(btn_w, btn_h, left_btn_x, top_btn_y).set_text("Multiplayer").set_action(launch_btn))
main_buttons.append(Button(btn_w, btn_h, mid_btn_x, top_btn_y).set_text("Local").set_action(launch_btn))
main_buttons.append(Button(btn_w, btn_h, mid_btn_x, center_btn_y).set_text("Règles").set_action(rules_btn))
main_buttons.append(Button(btn_w, btn_h, mid_btn_x, bottom_btn_y).set_text("Quitter").set_action(quit_btn))
main_buttons.append(Button(btn_w, btn_h, right_btn_x, bottom_btn_y).set_text("A propos").set_action(about_btn))

MAIN_MENU = True
RULES_MENU = False
ABOUT_MENU = False
while True:
    pygame.display.update()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if MAIN_MENU:
                for button in main_buttons:
                    if button.x <= mouse[0] <= button.x + button.width and button.y <= mouse[1] <= button.y + button.height:
                        button.action()

    WIN.blit(BACKGROUND, (0,0))

    if MAIN_MENU:
        for button in main_buttons:
            button.show()

    clock.tick(FPS)
