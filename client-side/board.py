"""Gestionnaire de plateau"""
#!/usr/bin/python3
import os
import sys
import pygame
import socket
from pygame.locals import *
from ttmc import *

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
        return 1 if self.rect.collidepoint(loc_mouse) else 0

    def obj_type(self):
        """Returns the object type"""
        return "button"

os.chdir(os.path.dirname(os.path.realpath(__file__)))

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"

pygame.init()

board_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

board_window.fill(WHITE)
pygame.display.set_caption('TTMC')
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

bg = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

text_font = pygame.font.SysFont("Corbel", 60)
text_font_small = pygame.font.SysFont("Corbel", 50)

objects = []

def start(players_list):
    """Démarrer le plateau"""
    stay = 1
    while stay:
        pygame.display.update()

        board_window.blit(bg, (0, 0))
        board_window.blit(BOARD_FAT, (SCREEN_WIDTH // 2 - BOARD_FAT.get_width() // 2, SCREEN_HEIGHT - BOARD_FAT.get_height()))

        # for dysp_obj in objects[state]:
        #     dysp_obj.show()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            stay = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                stay = 0

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         for dysp_obj in objects[state]:
            #             if dysp_obj.obj_type() == "button":
            #                 if dysp_obj.collide_mouse():
            #                     dysp_obj.action()

        clock.tick(FPS)

    pygame.quit()


def start_local():
    players_num = 0
    ask_text = text_font.render("Entrer le nombre de joueurs :", True, YELLOW)
    ask_rect = ask_text.get_rect()
    ask_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    text = ""
    done = 0
    while not done:
        pygame.display.update()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            players_num = 0
            break

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    if text:
                        players_num = int(text)
                        done = 1

                elif event.key == K_BACKSPACE:
                    text = text[:-1]

                else:
                    inp = event.unicode
                    if inp.isdigit():
                        text += str(inp)
                        if int(text) > 4:
                            text = "4"

        board_window.blit(bg, (0, 0))
        pygame.draw.rect(board_window, PURPLE, ask_rect, border_radius = 10)
        board_window.blit(ask_text, ask_rect)

        inp_text = text_font_small.render(text, True, YELLOW)
        inp_rect = inp_text.get_rect()
        inp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + ask_rect.height + 10)

        pygame.draw.rect(board_window, PURPLE, inp_rect, border_radius = 10)
        board_window.blit(inp_text, inp_rect)

        clock.tick(FPS)

    if players_num == 0:
        sys.exit()

    players_list = []
    for i in range(players_num):
        ask_text = text_font.render(f"Entrer le nom du joueur {i+1} :", True, YELLOW)
        ask_rect = ask_text.get_rect()
        ask_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        text = ""
        done = 0

        while not done:
            pygame.display.update()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_ESCAPE]:
                players_num = 0
                break

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        if not text:
                            text = f"Joueur {i+1}"

                        if not text in players_list:
                            players_list.append(text)
                            done = 1

                    elif event.key == K_BACKSPACE:
                        text = text[:-1]

                    else:
                        if len(text) < 10:
                            inp = event.unicode
                            if inp.isalpha():
                                text += str(inp)

            board_window.blit(bg, (0, 0))
            pygame.draw.rect(board_window, PURPLE, ask_rect, border_radius = 10)
            board_window.blit(ask_text, ask_rect)

            inp_text = text_font_small.render(text, True, YELLOW)
            inp_rect = inp_text.get_rect()
            inp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + ask_rect.height + 10)

            pygame.draw.rect(board_window, PURPLE, inp_rect, border_radius = 10)
            board_window.blit(inp_text, inp_rect)

            clock.tick(FPS)

    start(players_list)


def start_online():

    def new_server():
        pass


    def existing_server():
        s_num = 0
        ask_text = text_font.render("Entrer l'id du serveur :", True, YELLOW)
        ask_rect = ask_text.get_rect()
        ask_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        text = ""
        done = 0
        while not done:
            pygame.display.update()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_ESCAPE]:
                s_num = 0
                break

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        if len(text) == 4:
                            s_num = int(text)
                            done = 1

                    elif event.key == K_BACKSPACE:
                        text = text[:-1]

                    else:
                        inp = event.unicode
                        if inp.isdigit():
                            if int(text) < 4:
                                text += str(inp)

            board_window.blit(bg, (0, 0))
            pygame.draw.rect(board_window, PURPLE, ask_rect, border_radius = 10)
            board_window.blit(ask_text, ask_rect)

            inp_text = text_font_small.render(text, True, YELLOW)
            inp_rect = inp_text.get_rect()
            inp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + ask_rect.height + 10)

            pygame.draw.rect(board_window, PURPLE, inp_rect, border_radius = 10)
            board_window.blit(inp_text, inp_rect)

            clock.tick(FPS)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("cmi-game.ms-corporation.xyz", 80))
        s.setblocking(0)
        while True:
            try:
                msg = s.recv()

            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue

                else:
                    print(e)
                    sys.exit(1)

            finally:
                pass

    players_num = 0
    exis_s = Button(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 200, 50, board_window).set_text("Se connecter à un\nserveur existant").set_action(existing_server)
    new_s = Button(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 200, 50, board_window).set_text("Nouveau serveur").set_action(new_server)

    text = ""
    done = 0
    while not done:
        pygame.display.update()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            s_num = 0
            break

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    if len(text) == 4:
                        s_num = int(text)
                        done = 1

                elif event.key == K_BACKSPACE:
                    text = text[:-1]

                else:
                    inp = event.unicode
                    if inp.isdigit():
                        if int(text) < 4:
                            text += str(inp)

        board_window.blit(bg, (0, 0))
        pygame.draw.rect(board_window, PURPLE, ask_rect, border_radius = 10)
        board_window.blit(ask_text, ask_rect)

        inp_text = text_font_small.render(text, True, YELLOW)
        inp_rect = inp_text.get_rect()
        inp_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + ask_rect.height + 10)

        pygame.draw.rect(board_window, PURPLE, inp_rect, border_radius = 10)
        board_window.blit(inp_text, inp_rect)

        clock.tick(FPS)


# if len(sys.argv) > 1 and sys.argv[1] == "1":
#     start_online()

# else:
#     start_local()

start_local()
