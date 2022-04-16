"""init"""
import os
from pygame.locals import *
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

BACKGROUND = pygame.image.load(f"{actual_path}/background.jpg")
BOARD = pygame.image.load(f"{actual_path}/plateau.jpg")
BOARD_FAT = pygame.image.load(f"{actual_path}/plateau_fat.jpg")
ICON = pygame.image.load(f"{actual_path}/icon.png")
MENU_LOGO = pygame.image.load(f"{actual_path}/logo_accueil.png")

RULES1 = pygame.image.load(f"{actual_path}/règles1.jpg")
RULES2 = pygame.image.load(f"{actual_path}/règles2.jpg")
RULES3 = pygame.image.load(f"{actual_path}/règles3.jpg")
RULES4 = pygame.image.load(f"{actual_path}/règles4.jpg")

class Text:
    """Text constructor"""
    def __init__(self, x, y, text, window):
        self.x = x
        self.y = y
        self.text = text
        self.window = window
        self.font = "Corbel"
        self.size = 20
        self.text_color = YELLOW
        self.id = None
        self.has_back = 1
        self.back_color = PURPLE
        self.max_pline = 18
        self.is_active = 0

    def set_active(self, active):
        """Set the active state"""
        self.is_active = active
        return self

    def has_background(self, has_back, back_color = PURPLE):
        """Set the background"""
        self.has_back = has_back
        self.back_color = back_color
        return self

    def set_colors(self, text_color):
        """Setting color for the text"""
        self.text_color = text_color
        return self

    def set_max_pline(self, max_pline):
        """Set the max of char per line"""
        self.max_pline = max_pline
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

    def set_id(self, id_s):
        """Set the id"""
        self.id = id_s
        return self

    def get_height(self):
        """Render text"""
        text_font = pygame.font.SysFont(self.font, self.size)
        if self.max_pline != 0:
            height = 0
            for i in range(0, len(self.text), self.max_pline):
                message = text_font.render(self.text[i:i + self.max_pline], True, self.text_color)

                height += message.get_height()
                if self.has_back:
                    height += 20

        else:
            message = text_font.render(self.text, True, self.text_color)

            height = message.get_height()
            if self.has_back:
                height += 20

        return height

    def event(self, event):
        """Event"""

    def show(self):
        """Show text"""
        if self.is_active:
            text_font = pygame.font.SysFont(self.font, self.size)
            if self.max_pline != 0:
                for i in range(0, len(self.text), self.max_pline):
                    message = text_font.render(self.text[i:i + self.max_pline], True, self.text_color)

                    coord = (self.x - message.get_width() // 2, self.y - message.get_height() // 2 + i // self.max_pline * (message.get_height() + 20))

                    if self.has_back:
                        rect = pygame.Rect(coord[0] - 10, coord[1] - 10, message.get_width() + 20, message.get_height() + 20)
                        pygame.draw.rect(self.window, self.back_color, rect, border_radius=10)

                    self.window.blit(message, coord)

            else:
                message = text_font.render(self.text, True, self.text_color)

                coord = (self.x - message.get_width() // 2, self.y - message.get_height() // 2)

                if self.has_back:
                    rect = pygame.Rect(coord[0] - 10, coord[1] - 10, message.get_width() + 20, message.get_height() + 20)
                    pygame.draw.rect(self.window, self.back_color, rect, border_radius=10)

                self.window.blit(message, coord)

    def obj_type(self):
        """Returns the object type"""
        return "text"

    def get_id(self):
        """Returns the id"""
        return self.id


class Input(Text):
    """Input constructor"""
    def __init__(self, x, y, window):
        super().__init__(x, y, "", window)
        self.type = "anw"
        self.fun = None
        self.args = None
        self.max_num = -1
        self.min_num = -1

    def get_text(self):
        """Returns the text"""
        return self.text

    def set_action(self, action, *args):
        """Set the action"""
        self.fun = action
        self.args = args
        return self

    def action(self):
        """Call the action"""
        self.fun("{\"done\": \"1\", \"" + self.id + "\": \"" + self.text + "\"}", *self.args)

    def set_itype(self, type_s):
        """Set the type"""
        self.type = type_s
        return self

    def set_mm_num(self, max_num = -1, min_num = -1):
        """Set the max number"""
        self.max_num = max_num
        self.min_num = min_num
        return self

    def event(self, event):
        """Handle event"""
        if self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    self.action()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    inp = event.unicode
                    if (("a" in self.type and inp.isalpha()) or ("n" in self.type and inp.isdigit()) or ("w" in self.type and inp == " ")) and len(self.text) < self.max_pline:
                        self.text += inp

                    if self.text != "":
                        if self.max_num != -1 and self.type == "n" and int(self.text) > self.max_num:
                            self.text = str(self.max_num)

                        if self.min_num != -1 and self.type == "n" and int(self.text) < self.min_num:
                            self.text = str(self.min_num)

    def obj_type(self):
        """Returns the object type"""
        return "input"


class Button:
    """Button constructor"""
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.btn_color = PURPLE
        self.text_color = YELLOW
        self.btn_color_hovered = YELLOW
        self.text_color_hovered = PURPLE
        self.text = ""
        self.font = "Corbel"
        self.size = 20
        self.func = None
        self.args = None
        self.rect = None
        self.id = None
        self.is_active = 0
        self.render_text()

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

    def set_font(self, font):
        """Set font for the text"""
        self.font = font
        return self

    def set_size(self, size):
        """Set font size for the text"""
        self.size = size
        return self

    def set_active(self, active):
        """Set active state"""
        self.is_active = active
        return self

    def set_action(self, func, *args):
        """Set action of the button"""
        self.func = func
        self.args = args
        return self

    def action(self):
        """Execute the action of the button"""
        if self.func is not None:
            self.func(*self.args)

    def render_text(self, hovered = 0):
        """Render text"""
        button_font = pygame.font.SysFont(self.font, self.size)
        if hovered:
            message = button_font.render(self.text, True, self.text_color_hovered)

        else:
            message = button_font.render(self.text, True, self.text_color)

        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

        return message

    def event(self, event):
        """Event of the button"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.collide_mouse():
                self.action()

    def show(self):
        """Show button"""
        if self.is_active:
            collide = self.collide_mouse()
            message = self.render_text(collide)

            if collide:
                pygame.draw.rect(self.window, self.btn_color_hovered, self.rect, border_radius = 30)

            else:
                pygame.draw.rect(self.window, self.btn_color, self.rect, border_radius = 30)

            self.window.blit(message, (self.x - message.get_width()/2, self.y - message.get_height()/2))

    def collide_mouse(self):
        """Check if mouse is over the button"""
        loc_mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(loc_mouse)

    def set_id(self, id_s):
        """Set the id"""
        self.id = id_s
        return self

    def obj_type(self):
        """Returns the object type"""
        return "button"


class Image:
    """Image constructor"""
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.id = None
        self.window = window

    def show(self):
        """Show button"""
        self.window.blit(self.image, (self.x - self.image.get_width()/2, self.y  - self.image.get_height()/2))

    def set_id(self, id_s):
        """Set the id"""
        self.id = id_s
        return self

    def obj_type(self):
        """Returns the object type"""
        return "image"


class Map:
    "Map display and settings"
    def __init__(self, window):
        self.window = window

        self.little_board = pygame.transform.scale(BOARD, (int(BOARD.get_width()*0.4), int(BOARD.get_height()*0.4)))
        self.lmap_x = SCREEN_WIDTH - self.little_board.get_width() - 20
        self.lmap_y = 20
        self.lmap_rect = pygame.Rect(self.lmap_x, self.lmap_y, self.little_board.get_width(), self.little_board.get_height())

        self.big_board = BOARD_FAT
        self.bmap_x = self.lmap_x - 20 - self.big_board.get_width()
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
        self.s_is_clicked = 0

        self.piece_radius = 0.05 * self.big_board.get_width()
        self.pieces_list = {}

    def add_piece(self, player_name):
        """Add piece to the map"""
        colors_list = [RED, BLUE, GREEN, ORANGE]
        self.pieces_list[player_name] = {"pos": 0, "color": colors_list[len(self.pieces_list)]}

    def move_piece(self, player_name, case_num):
        """Move piece on the map"""
        self.pieces_list[player_name]["pos"] += case_num
        if self.pieces_list[player_name]["pos"] > 40:
            self.pieces_list[player_name]["pos"] = 41

    def get_piece_info(self, player_name):
        """Return info of a piece"""
        return self.pieces_list[player_name]

    def scroll(self):
        """Scrolling function for the map"""
        if self.scrolli_collide_mouse():
            if self.s_is_clicked:
                self.bmap_y += (self.last_mouse_y - pygame.mouse.get_pos()[1]) * (1 / self.lob_ratio)
                self.last_mouse_y = pygame.mouse.get_pos()[1]

        if self.bmap_y > self.bmap_max_y:
            self.bmap_y = self.bmap_max_y

        elif self.bmap_y < self.bmap_min_y:
            self.bmap_y = self.bmap_min_y

    def event(self,event):
        """Event of the map"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.scrolli_collide_mouse():
                    self.s_is_clicked = 1
                    self.last_mouse_y = pygame.mouse.get_pos()[1]

            if self.lmap_collide_mouse() or self.bmap_collide_mouse():
                if event.button == 4:
                    self.bmap_y += 50

                elif event.button == 5:
                    self.bmap_y -= 50

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.s_is_clicked = 0

    def show(self):
        """Show map"""
        self.window.blit(self.little_board, (self.lmap_x, self.lmap_y))
        self.window.blit(self.scrolli, (self.lmap_x, 20 + (self.bmap_max_y - self.bmap_y) * self.lob_ratio))
        self.window.blit(self.big_board, (self.bmap_x, self.bmap_y))

        for player_name in self.pieces_list:
            pos = MATRICE_COORD_CASES[self.pieces_list[player_name]["pos"]]
            pos_x = pos[0] * self.big_board.get_width() + self.bmap_x
            pos_y = pos[1] * self.big_board.get_height() + self.bmap_y
            pygame.draw.circle(self.window, self.pieces_list[player_name]["color"], (pos_x, pos_y), self.piece_radius)

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


MATRICE_COORD_CASES = [(0.9, 0.94), (0.75, 0.94), (0.63, 0.92), (0.53, 0.86),
                       (0.38, 0.87), (0.28, 0.94), (0.13, 0.92), (0.1, 0.83),
                       (0.1, 0.72), (0.2, 0.64), (0.35, 0.68), (0.43, 0.74),
                       (0.57, 0.75), (0.63, 0.68), (0.77, 0.66), (0.87, 0.63),
                       (0.87, 0.54), (0.78, 0.5), (0.67, 0.53), (0.55, 0.61),
                       (0.48, 0.55), (0.4, 0.5), (0.28, 0.54), (0.15, 0.56),
                       (0.1, 0.49), (0.12, 0.4), (0.23, 0.34), (0.37, 0.37),
                       (0.5, 0.43), (0.62, 0.39), (0.75, 0.34), (0.88, 0.32),
                       (0.8, 0.25), (0.65, 0.25), (0.48, 0.25), (0.32, 0.25),
                       (0.15, 0.25), (0.08, 0.17), (0.17, 0.09), (0.32, 0.07),
                       (0.47, 0.12)]

POSSIBLE_TYPES = ["imp", "mat", "sco", "cvp", "cha", "pla", "csp", "win"]
CASES_TYPES = [0, 1, 2, 3, 0, 4, 1, 2, 5, 6, 3, 5, 2, 0, 1, 4, 2, 5, 6, 1, 0,
               2, 5, 0, 5, 1, 3, 4, 2, 5, 0, 1, 2, 5, 2, 1, 6, 0, 4, 1, 7]