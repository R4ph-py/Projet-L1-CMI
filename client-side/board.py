"""Gestionnaire de plateau"""
#!/usr/bin/python3
import os
import sys
import pygame
import socket
import json
from time import sleep, time
from pygame.locals import *
from ttmc import *

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

def difficulty_choose(diff):
    """Difficulté choisie"""
    return diff

game_objs = [Map(board_window)]
map_x = game_objs[0].bmap_x
game_objs.append(Text(map_x // 2, SCREEN_HEIGHT // 6, "Tour de X", board_window).set_colors(YELLOW).set_size(100).set_id("tour").has_background(1, PURPLE))
game_objs.append(Text(map_x // 2, SCREEN_HEIGHT // 3, "Tu te mets combien en X ?", board_window).set_colors(YELLOW).set_size(60).set_id("ttmcQ").has_background(1, PURPLE))

game_objs.append(Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window).set_text("1").set_size(40).set_action(difficulty_choose, 1))
game_objs.append(Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window).set_text("2").set_size(40).set_action(difficulty_choose, 2))
game_objs.append(Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window).set_text("3").set_size(40).set_action(difficulty_choose, 3))
game_objs.append(Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window).set_text("4").set_size(40).set_action(difficulty_choose, 4))
game_objs.append(Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window).set_text("5").set_size(40).set_action(difficulty_choose, 5))
game_objs.append(Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window).set_text("6").set_size(40).set_action(difficulty_choose, 6))
game_objs.append(Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window).set_text("7").set_size(40).set_action(difficulty_choose, 7))
game_objs.append(Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window).set_text("8").set_size(40).set_action(difficulty_choose, 8))
game_objs.append(Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window).set_text("9").set_size(40).set_action(difficulty_choose, 9))
game_objs.append(Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window).set_text("10").set_size(40).set_action(difficulty_choose, 10))

game_objs.append(Text(map_x // 2, SCREEN_HEIGHT // 2, "", board_window).set_colors(YELLOW).set_size(50).set_id("qPoser").has_background(1, PURPLE).set_max_pline(26))

def start(players_list):
    """Démarrer le plateau"""
    stay = 1
    turn_num = 0
    while stay:
        pygame.display.update()

        board_window.blit(bg, (0, 0))

        player_turn = players_list[turn_num % len(players_list)]

        for dysp_obj in game_objs:
            dysp_obj.show()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                if button == 1:
                    for dysp_obj in game_objs:
                        if dysp_obj.obj_type() == "button":
                            if dysp_obj.collide_mouse():
                                dysp_obj.action()

                        if dysp_obj.obj_type() == "map":
                            dysp_obj.scroll(button)

                elif button == 4 or button == 5:
                    for dysp_obj in game_objs:
                        if dysp_obj.obj_type() == "map":
                            dysp_obj.scroll(button)

            elif event.type == pygame.MOUSEBUTTONUP:
                button = event.button
                if button == 1:
                    for dysp_obj in game_objs:
                        if dysp_obj.obj_type() == "map":
                            dysp_obj.released_mouse()

            for dysp_obj in game_objs:
                if dysp_obj.obj_type() == "map":
                    dysp_obj.scroll()

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
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    if text:
                        players_num = int(text)
                        if players_num > 1:
                            done = 1

                elif event.key == K_BACKSPACE:
                    text = text[:-1]

                else:
                    inp = event.unicode
                    if inp.isdigit():
                        text = str(inp)
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
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

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
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

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

        try:
            data = s.recv()
            reply = data.decode('utf-8')

            try:
                if not json.loads(reply)["ask"] == "version":
                    raise json.decoder.JSONDecodeError

                s.send(str.encode(json.dumps({"asw": GAME_VERSION})))
                data = s.recv()
                reply = data.decode('utf-8')
                data_j = json.loads(reply)

                if data_j["ask"] and data_j["ask"] == "new or connect":
                    s.send(str.encode(json.dumps({"asw": "connect", "server_id": s_num})))
                    data = s.recv()
                    reply = data.decode('utf-8')
                    data_j = json.loads(reply)

                elif data_j["error"] and data_j["error"] == "invalid answer":
                    print("Not concording versions")
                    raise json.decoder.JSONDecodeError

                else:
                    raise json.decoder.JSONDecodeError

            except json.decoder.JSONDecodeError:
                s.close()

            except KeyError:
                s.close()

            # try:
            #     msg = s.recv()

            # except socket.error as e:
            #     err = e.args[0]
            #     if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            #         print('No data available')
            #         continue

            #     else:
            #         print(e)
            #         pygame.quit()
            #         sys.exit(1)

            # finally:
            #     try:
            #         if json.loads(msg.decode("utf-8"))["ask"] == "version":
            #             s.send(json.dumps({"asw": VERSION}).encode())

        except socket.error as cl_err:
            print(f"Connexion au serveur fermée : {cl_err}")
            s.close()

    players_num = 0
    exis_s = Button(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 200, 50, board_window).set_text("Se connecter à un serveur existant").set_action(existing_server)
    new_s = Button(SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 2, 200, 50, board_window).set_text("Nouveau serveur").set_action(new_server)

    text = ""
    done = 0
    while not done:
        pygame.display.update()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if exis_s.collide_mouse():
                    existing_server()
                    done = 1

                elif new_s.collide_mouse():
                    new_server()
                    done = 1

        board_window.blit(bg, (0, 0))
        exis_s.show()
        new_s.show()

        clock.tick(FPS)


# if len(sys.argv) > 1 and sys.argv[1] == "1":
#     start_online()

# else:
#     start_local()

start(["nifvivre", "nifvivre"])
