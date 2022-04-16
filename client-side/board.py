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

def coms(to_send, to_who = "board"):
    """Communication board and manager process"""
    global TO_BOARD
    global TO_PROCESS
    if to_who == "board":
        TO_BOARD = to_send

    else:
        TO_PROCESS = to_send


num_p_objs = {0: Text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "Entrer le nombre de joueurs :", board_window).set_size(60).set_max_pline(0).set_active(1)}
num_p_objs[1] = Input(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + num_p_objs[0].get_height(), board_window).set_size(50).set_itype("n").set_id("num p").set_action(coms, "process").set_mm_num(4, 2).set_active(1)

p_name_objs = {0: Text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "Entrer le nom du joueur X :", board_window).set_size(60).set_max_pline(0).set_active(1)}
p_name_objs[1] = Input(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + p_name_objs[0].get_height(), board_window).set_size(50).set_itype("a").set_id("name p").set_action(coms, "process").set_mm_num(7).set_active(1)

def difficulty_choose(diff):
    """Difficulté choisie"""
    global TO_BOARD
    TO_BOARD = "{\"difficulty\": \"" + str(diff) + "\"}"

game_objs = {"map": Map(board_window)}
map_x = game_objs["map"].bmap_x
map_w = game_objs["map"].big_board.get_width()

game_objs["tour"] = Text(map_x // 2, SCREEN_HEIGHT // 7, "Tour de 1234567", board_window).set_size(100).set_id("tour").set_active(1)
game_objs["j2_t"] = Text(map_x + map_w + (SCREEN_WIDTH - (map_x + map_w)) // 2, SCREEN_HEIGHT // 3*2, "Joueur 2", board_window).set_size(45).set_id("p2").set_colors(BLUE).has_background(1, WHITE).set_active(1)
j2_t_height = game_objs["j2_t"].get_height()
game_objs["j1_t"] = Text(map_x + map_w + (SCREEN_WIDTH - (map_x + map_w)) // 2, SCREEN_HEIGHT // 3*2 - j2_t_height - 20, "", board_window).set_size(45).set_id("p1").set_colors(RED).has_background(1, WHITE).set_active(1)
game_objs["j3_t"] = Text(map_x + map_w + (SCREEN_WIDTH - (map_x + map_w)) // 2, SCREEN_HEIGHT // 3*2 + j2_t_height + 20, "", board_window).set_size(45).set_id("p3").set_colors(GREEN).has_background(1, WHITE).set_active(1)
game_objs["j4_t"] = Text(map_x + map_w + (SCREEN_WIDTH - (map_x + map_w)) // 2, SCREEN_HEIGHT // 3*2 + 2 * j2_t_height + 40, "", board_window).set_size(45).set_id("p4").set_colors(ORANGE).has_background(1, WHITE).set_active(1)

game_objs["ttmc_q"] = Text(map_x // 2, SCREEN_HEIGHT // 4, "Tu te mets combien en X ?", board_window).set_size(60).set_id("ttmc_q").set_max_pline(0).set_max_pline(25)
game_objs["q_poser"] = Text(map_x // 2, SCREEN_HEIGHT // 5 * 2, "", board_window).set_size(40).set_id("q_poser").set_max_pline(26)
game_objs["asw_inp"] = Input(map_x // 2, SCREEN_HEIGHT // 2, board_window).set_size(40).set_id("asw_inp").set_max_pline(30).set_action(coms)

game_objs["btn_d0"] = Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)
game_objs["btn_d1"] = Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)
game_objs["btn_d2"] = Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)
game_objs["btn_d3"] = Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)
game_objs["btn_d4"] = Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 4, 100, 75, board_window)
game_objs["btn_d5"] = Button(map_x // 6 * 1, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window)
game_objs["btn_d6"] = Button(map_x // 6 * 2, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window)
game_objs["btn_d7"] = Button(map_x // 6 * 3, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window)
game_objs["btn_d8"] = Button(map_x // 6 * 4, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window)
game_objs["btn_d9"] = Button(map_x // 6 * 5, SCREEN_HEIGHT // 6 * 5, 100, 75, board_window)

game_objs["r_asw"] = Text(map_x // 2, SCREEN_HEIGHT // 20 * 12, "", board_window).set_size(40).set_id("r_asw").set_max_pline(40)
game_objs["vote"] = Text(map_x // 2, SCREEN_HEIGHT // 10 * 8, "La réponse donnée est elle valide ? (demandez à tout le monde)", board_window).set_size(32).set_id("vote").set_max_pline(40)
game_objs["vote_btn1"] = Button(map_x // 3, SCREEN_HEIGHT // 10 * 9, 100, 50, board_window).set_text("Oui").set_id("vote_btn1").set_action(coms, "{\"vote_btn1\": \"1\"}")
game_objs["vote_btn2"] = Button(map_x // 3 * 2, SCREEN_HEIGHT // 10 * 9, 100, 50, board_window).set_text("Non").set_id("vote_btn2").set_action(coms, "{\"vote_btn2\": \"1\"}")

def quit():
    """Quitter le jeu"""
    sys.exit()

win_objs = {"win_t": Text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "", board_window).set_size(60).set_id("win_t").set_max_pline(0).set_active(1)}
win_objs["win_btn1"] = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 200, 50, board_window).set_text("Fin").set_id("win_btn1").set_size(50).set_action(quit).set_active(1)

for i in range(10):
    game_objs[f"btn_d{i}"].set_text(f"{i + 1}").set_size(40).set_action(difficulty_choose, i + 1).set_id(f"btn_d{i}")


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

    time.sleep(0.1)

    TO_BOARD = "{\"turn\": \"0\"}"


def start(is_online = 0):
    """Démarrer le plateau"""
    global TO_BOARD
    global TO_PROCESS

    if is_online == 1:
        # _thread.start_new_thread(start_online, ())
        pass

    else:
        _thread.start_new_thread(start_local, ())

    stay = 1
    started = 0
    last_read = ""
    turn_of = ""
    turn = 0

    while stay:
        pygame.display.update()

        v_read = json.loads(TO_BOARD)

        board_window.blit(bg, (0, 0))

        if not last_read == v_read:
            if not started:
                if "action" in v_read:
                    if v_read["action"] == "ask":

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
                        for j in range(len(players_list)):
                            game_objs[f"j{j+1}_t"].set_text(players_list[j])
                            game_objs["map"].add_piece(players_list[j])

                        objs = game_objs

            else:

                if "turn" in v_read:
                    turn = int(v_read["turn"])
                    turn_of = players_list[turn%len(players_list)]
                    objs["tour"].set_text(f"Tour de {turn_of}")

                    piece = objs["map"].get_piece_info(turn_of)
                    case_num = piece["pos"]
                    case_type = POSSIBLE_TYPES[CASES_TYPES[case_num]]
                    card = {"category": "categorie", "10": {"question": "diff1q", "reponse": "diff1r"}, "2": {"question": "diff2q", "reponse": "diff2r"}} #séléctionner une carte aléatoire
                    if case_type == "imp":
                        pass

                    elif case_type == "mat":
                        pass

                    elif case_type == "sco":
                        pass

                    elif case_type == "cpv":
                        pass

                    elif case_type == "cha":
                        pass

                    elif case_type == "pla":
                        pass

                    elif case_type == "csp":
                        pass

                    elif case_type == "win":
                        pass

                    category = card["category"]
                    objs["ttmc_q"].set_text(f"Tu te mets combien en {category} ?").set_active(1)
                    for j in range(10):
                        objs[f"btn_d{j}"].set_active(1)

                if "difficulty" in v_read:
                    diff = v_read["difficulty"]
                    objs["ttmc_q"].set_text(f"Tu te mets {diff} en {category}")
                    for j in range(10):
                        objs[f"btn_d{j}"].set_active(0)

                    question = card[diff]["question"] #prendre la question correspondant à la difficulté sur la carte choisie
                    objs["q_poser"].set_text(question).set_active(1)
                    objs["asw_inp"].set_active(1)

                if "asw_inp" in v_read:
                    asw = v_read["asw_inp"]
                    objs["asw_inp"].set_text(asw).set_active_inp(0)
                    asw = card[diff]["reponse"]
                    objs["r_asw"].set_text(f"Réponse : {asw}").set_active(1)
                    objs["vote"].set_active(1)
                    objs["vote_btn1"].set_active(1)
                    objs["vote_btn2"].set_active(1)

                if "vote_btn1" in v_read:
                    objs["q_poser"].set_text("").set_active(0)
                    objs["asw_inp"].set_active_inp(1).set_active(0)
                    objs["r_asw"].set_active(0)
                    objs["vote"].set_active(0)
                    objs["vote_btn1"].set_active(0)
                    objs["vote_btn2"].set_active(0)
                    if piece["pos"] == 40:
                        objs = win_objs
                        objs["win_t"].set_text(f"{turn_of} a gagné !")

                    else:
                        objs["map"].move_piece(turn_of, int(diff))
                        TO_BOARD = "{\"turn\": \"" + str(turn + 1) + "\"}"

                if "vote_btn2" in v_read:
                    objs["q_poser"].set_text("").set_active(0)
                    objs["asw_inp"].set_active_inp(1).set_active(0)
                    objs["r_asw"].set_active(0)
                    objs["vote"].set_active(0)
                    objs["vote_btn1"].set_active(0)
                    objs["vote_btn2"].set_active(0)
                    TO_BOARD = "{\"turn\": \"" + str(turn + 1) + "\"}"

            last_read = v_read

        for name, obj in objs.items():
            if name == "map":
                obj.scroll()

            obj.show()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            for _, obj in objs.items():
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
