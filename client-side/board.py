"""Gestionnaire de plateau"""
#!/usr/bin/python3
import os
import sys
import pygame
import socket
import json
import _thread
import time
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

TO_BOARD = "{\"blank\": \"blank\"}"
TO_PROCESS = "{\"blank\": \"blank\"}"

def coms(to_send, to_who):
    """Communication between board and manager process"""
    global TO_BOARD
    global TO_PROCESS
    if to_who == "board":
        TO_BOARD = to_send

    if to_who == "process":
        TO_PROCESS = to_send


num_p_objs = [Text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "Entrer le nombre de joueurs :", board_window).set_size(60).set_max_pline(0)]
num_p_objs.append(Input(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + num_p_objs[0].get_height(), board_window).set_size(50).set_itype("n").set_id("num p").set_action(coms, "process").set_mm_num(4, 2))

p_name_objs = [Text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "Entrer le nom du joueur X :", board_window).set_size(60).set_max_pline(0)]
p_name_objs.append(Input(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + p_name_objs[0].get_height(), board_window).set_size(50).set_itype("a").set_id("name p").set_action(coms, "process").set_mm_num(7))

def difficulty_choose(diff):
    """Difficulté choisie"""
    return diff

game_objs = [Map(board_window)]
map_x = game_objs[0].bmap_x

game_objs.append(Text(map_x // 2, SCREEN_HEIGHT // 7, "Tour de 1234567", board_window).set_size(100).set_id("tour"))

question_objs   =   [Text(map_x // 2, SCREEN_HEIGHT // 3, "Tu te mets combien en X ?", board_window).set_size(60).set_id("ttmcQ").set_max_pline(0)]
question_objs.append(Text(map_x // 2, SCREEN_HEIGHT // 2, "", board_window).set_size(50).set_id("qPoser").set_max_pline(26))
question_objs.append(Input(map_x // 2, SCREEN_HEIGHT // 3 * 2, board_window))

difficulty_btns   =   [Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)]
difficulty_btns.append(Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window))
difficulty_btns.append(Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window))

for i in range(10):
    difficulty_btns[i].set_text(f"{i}").set_size(40).set_action(difficulty_choose, i).set_id(f"difficulty_{i}")


def start_local():
    """Démarrer le gestionnaire local"""
    global TO_BOARD
    global TO_PROCESS

    players_num = 0

    TO_BOARD = "{\"action\": \"ask\", \"num p\": \"\"}"

    done = 0
    while not done:
        v_read = json.loads(TO_PROCESS)
        if "done" in v_read:
            done = v_read["done"]
            if done:
                if v_read["num p"] == "":
                    done = 0
                    TO_PROCESS = "{\"blank\": \"blank\"}"

                else:
                    players_num = int(v_read["num p"])

    if players_num == 0:
        sys.exit()

    TO_PROCESS = "{\"blank\": \"blank\"}"

    players_list = []
    for j in range(players_num):
        TO_BOARD = "{\"action\": \"ask\", \"name p\": \"" + str(j+1) + "\"}"

        done = 0
        while not done:
            v_read = json.loads(TO_PROCESS)
            if "done" in v_read:
                done = v_read["done"]
                if done:
                    if v_read["name p"] == "":
                        v_read["name p"] = "Joueur " + str(j+1)

                    players_list.append(v_read["name p"])

        TO_PROCESS = "{\"blank\": \"blank\"}"

    TO_BOARD = "{\"action\": \"start\", \"players\": \"" + str(players_list) + "\"}"

    while 1:
        v_read = json.loads(TO_BOARD)
        if "action" in v_read:
            if v_read["action"] == "start":
                break


def start(is_online = 0):
    """Démarrer le plateau"""
    if is_online == 1:
        # _thread.start_new_thread(start_online, ())
        pass

    else:
        _thread.start_new_thread(start_local, ())

    stay = 1
    started = 0
    last_read = ""

    while stay:
        pygame.display.update()

        v_read = json.loads(TO_BOARD)

        board_window.blit(bg, (0, 0))

        try:
            if not last_read == v_read:
                if "action" in v_read:
                    if v_read["action"] == "ask":

                        if not started:
                            if "num p" in v_read:
                                objs = num_p_objs
                                objs[1].set_active(1)

                            elif "name p" in v_read:
                                num = v_read["name p"]
                                objs = p_name_objs
                                objs[0].set_text(f"Entrer le nom du joueur {num} :")
                                objs[1].set_active(1)

                    elif v_read["action"] == "start":
                        started = 1
                        players_list = v_read["players"]
                        players_list = players_list.replace("[", "").replace("]", "").replace("\'", "").split(", ")
                        objs = game_objs

                    if "turn" in v_read:
                        objs = game_objs
                        objs[1].set_text(f"Tour de {players_list[v_read['turn']%len(players_list)]}")

                last_read = v_read

        except ValueError:
            pass

        for obj in objs:
            if obj.obj_type() == "map":
                obj.scroll()

            obj.show()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            for obj in objs:
                obj.event(event)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)

    pygame.quit()


if len(sys.argv) > 1 and sys.argv[1] == "1":
    start(1)

else:
    start()
