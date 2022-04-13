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

FPS = 30

BACKGROUND = pygame.image.load(f"{actual_path}/background.jpg")
BOARD = pygame.image.load(f"{actual_path}/plateau.jpg")
BOARD_FAT = pygame.image.load(f"{actual_path}/plateau_fat.jpg")
ICON = pygame.image.load(f"{actual_path}/icon.png")
MENU_LOGO = pygame.image.load(f"{actual_path}/logo_accueil.png")

RULES1 = pygame.image.load(f"{actual_path}/règles1.png")
RULES2 = pygame.image.load(f"{actual_path}/règles2.png")
RULES3 = pygame.image.load(f"{actual_path}/règles3.png")
RULES4 = pygame.image.load(f"{actual_path}/règles4.png")

class Text:
    """Text constructor"""
    def __init__(self, x, y, text, window):
        self.x = x
        self.y = y
        self.text = text
        self.window = window
        self.font = "Corbel"
        self.size = 20
        self.text_color = BLACK
        self.id = None
        self.has_back = False
        self.back_color = WHITE
        self.max_pline = 18

    def has_background(self, has_back, back_color = WHITE):
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

    def show(self):
        """Show text"""
        if self.max_pline != 0:
            text_font = pygame.font.SysFont(self.font, self.size)
            for i in range(0, len(self.text), self.max_pline):
                message = text_font.render(self.text[i:i + self.max_pline], True, self.text_color)

                coord = (self.x - message.get_width() // 2, self.y - message.get_height() // 2 + i // self.max_pline * (message.get_height() + 20))

                if self.has_back:
                    rect = pygame.Rect(coord[0] - 10, coord[1] - 10, message.get_width() + 20, message.get_height() + 20)
                    pygame.draw.rect(self.window, self.back_color, rect, border_radius=10)

                self.window.blit(message, coord)

        else:
            text_font = pygame.font.SysFont(self.font, self.size)
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
    def __init__(self, x, y, text, window, active = False):
        super().__init__(x, y, text, window)
        self.is_active = active

    def actualise(self, event):
        """Actualise the input"""
        if self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    inp = event.unicode
                    if inp.isalpha() or inp.isdigit() or inp == " ":
                        self.text += inp

    def set_active(self, active):
        """Set the active state"""
        self.is_active = active
        return self

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

    def show(self):
        """Show button"""

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
        self.window.blit(self.image, (self.x - image.get_width()/2, self.y  - image.get_height()/2))

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
        self.window.blit(self.scrolli, (self.lmap_x, 20 + (self.bmap_max_y - self.bmap_y) * self.lob_ratio))
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
