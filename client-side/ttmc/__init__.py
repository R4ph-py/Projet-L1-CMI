"""init"""
import os
import pygame
from screeninfo import get_monitors

actual_path = os.path.dirname(__file__)

# Récupérer les dimensions de l'écran
if len(get_monitors()) == 1:
    SCREEN_WIDTH = get_monitors()[0].width
    SCREEN_HEIGHT = get_monitors()[0].height

else:
    for monitor in get_monitors():
        if monitor.is_primary:
            SCREEN_WIDTH = monitor.width
            SCREEN_HEIGHT = monitor.height

GAME_VERSION = 1.0

WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480 + 230

BOARD_WIDTH, BOARD_HEIGHT = 612, 1029

# Couleurs des cases
RED = (139,0,0)
GREEN = (0,255,127)
BLUE = (0,191,255)
ORANGE = (255,140,0)
PURPLE = (128,0,128)
YELLOW = (255,215,0)
BLACK = (0, 0, 0)

# Autres couleurs
WHITE = (255, 255, 255)

FPS = 60

BACKGROUND = pygame.image.load(f"{actual_path}/Background.jpg")
BOARD = pygame.image.load(f"{actual_path}/Plateau.jpg")
BOARD_FAT = pygame.image.load(f"{actual_path}/Plateau_fat.jpg")
ICON = pygame.image.load(f"{actual_path}/icon.png")
MENU_LOGO = pygame.image.load(f"{actual_path}/logo_accueil.png")

class Text:
    """Text constructor"""
    def __init__(self, x, y, text, window):
        self.x = x
        self.y = y
        self.text = text
        self.font = "Corbel"
        self.size = 20
        self.text_color = BLACK
        self.window = window

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

        self.window.blit(message, (self.x - message.get_width() // 2, self.y - message.get_height() // 2))

    def obj_type(self):
        """Returns the object type"""
        return "text"


class Button:
    """Button constructor"""
    def __init__(self, x, y, width, height, window):
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
        self.window = window

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
            pygame.draw.rect(self.window, self.btn_color_hovered, self.rect, border_radius = 30)
            message = button_font.render(self.text, True, self.text_color_hovered)

        else:
            pygame.draw.rect(self.window, self.btn_color, self.rect, border_radius = 30)
            message = button_font.render(self.text, True, self.text_color)

        self.window.blit(message, (self.x + self.width/2 - message.get_width()/2, self.y + self.height/2 - message.get_height()/2))

    def collide_mouse(self):
        """Check if mouse is over the button"""
        loc_mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(loc_mouse)

    def obj_type(self):
        """Returns the object type"""
        return "button"


class Map:
    "Map display and settings"
    def __init__(self, window):
        self.window = window

        self.little_board = pygame.transform.scale(BOARD, (int(BOARD.get_width()*0.4), int(BOARD.get_height()*0.4)))
        self.lmap_x = SCREEN_WIDTH - self.little_board.get_width()
        self.lmap_y = 0
        self.lmap_rect = pygame.Rect(self.lmap_x, self.lmap_y, self.little_board.get_width(), self.little_board.get_height())

        self.big_board = BOARD_FAT
        self.bmap_x = SCREEN_WIDTH // 2 - self.big_board.get_width() // 2
        self.bmap_y = SCREEN_HEIGHT - self.big_board.get_height()
        self.bmap_rect = pygame.Rect(self.bmap_x, self.bmap_y, self.big_board.get_width(), self.big_board.get_height())
        self.bmap_min_y = self.bmap_y
        self.bmap_max_y = 0
        self.bmap_hidden_h = self.big_board.get_height() - SCREEN_HEIGHT

        self.lob_ratio = self.little_board.get_height() / self.big_board.get_height()

        self.scrolli = pygame.Surface((self.little_board.get_width(), self.little_board.get_height() - (self.bmap_hidden_h * self.lob_ratio)))
        self.scrolli.set_alpha(128)
        self.scrolli.fill(BLACK)

        self.last_mouse_y = 0
        self.s_is_clicked = False

    def scroll(self, button = 0):
        """Scrolling function for the map"""
        if self.lmap_collide_mouse() or self.bmap_collide_mouse():
            if button == 4:
                self.bmap_y += 50

            elif button == 5 and self.bmap_y > self.bmap_min_y:
                self.bmap_y -= 50

        if self.scrolli_collide_mouse():
            if self.s_is_clicked:
                self.bmap_y += (self.last_mouse_y - pygame.mouse.get_pos()[1]) * (1 / self.lob_ratio)
                self.last_mouse_y = pygame.mouse.get_pos()[1]

            elif button == 1:
                self.s_is_clicked = True
                self.last_mouse_y = pygame.mouse.get_pos()[1]

        if self.bmap_y > self.bmap_max_y:
            self.bmap_y = self.bmap_max_y

        elif self.bmap_y < self.bmap_min_y:
            self.bmap_y = self.bmap_min_y

    def released_mouse(self):
        """Mouse released"""
        self.s_is_clicked = False

    def show(self):
        """Show map"""
        self.window.blit(self.little_board, (self.lmap_x, self.lmap_y))
        self.window.blit(self.scrolli, (self.lmap_x, (self.bmap_max_y - self.bmap_y) * self.lob_ratio))
        self.window.blit(self.big_board, (self.bmap_x, self.bmap_y))
        return self

    def add_piece(self, player_name):
        """Add piece to the map"""

    def lmap_collide_mouse(self):
        """Check if mouse is over the little map"""
        loc_mouse = pygame.mouse.get_pos()
        return self.lmap_rect.collidepoint(loc_mouse)

    def bmap_collide_mouse(self):
        """Check if mouse is over the little map"""
        loc_mouse = pygame.mouse.get_pos()
        return self.bmap_rect.collidepoint(loc_mouse)

    def scrolli_collide_mouse(self):
        """Check if mouse is over the scroll indicator"""
        loc_mouse = pygame.mouse.get_pos()
        scrolli_rect = pygame.Rect(self.lmap_x, (self.bmap_max_y - self.bmap_y) * self.lob_ratio, self.little_board.get_width(), self.little_board.get_height() - self.bmap_hidden_h * self.lob_ratio)
        return scrolli_rect.collidepoint(loc_mouse)

    def obj_type(self):
        """Returns the object type"""
        return "map"
