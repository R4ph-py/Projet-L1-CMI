#!/bin/python3
"""Server module"""
import socket
import random
import json
import _thread
import time

GAME_VERSION = 1.0

SERVERS_LIST = {}

server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))
    exit()

class Server:
    """Class pour un serveur"""
    def __init__(self, server_id, exp_c_num):
        self.id = server_id
        self.clients = {}
        self.todo_action = None
        self.done_actions = []
        self.clients_amnt = exp_c_num
        self.game_launched = 0
        self.removed_clients = []
        self.clients_num = {}

    def add_client(self, client, address):
        """Ajoute un client au serveur"""
        if not self.game_launched:
            self.clients_num = len(self.clients - 1)

        elif not address in self.removed_clients:
            return 0

        self.clients[address] = client
        return self

    def test_clients(self):
        """Envoie un ping à tous les clients"""
        for adr, clnt in self.clients.items():
            try:
                clnt.ping()

            except socket.error:
                self.remove_client(adr)

    def remove_client(self, address):
        """Enlève un client au serveur"""
        try:
            self.clients[address].close()

        finally:
            del self.clients[address]
            self.removed_clients.append(address)

    def send_to(self, address, message):
        """Envoie un message à un client du serveur en fonction de son adresse"""
        for adr, clnt in self.clients.items():
            if adr == address:

                try:
                    clnt.send(str.encode(message))

                except socket.error:
                    self.remove_client(adr)

                break

    def send_all(self, message):
        """Envoie un message à tous les clients du serveur"""
        for adr, clnt in self.clients.items():
            try:
                clnt.send(str.encode(message))

            except socket.error:
                self.remove_client(adr)

    def start(self):
        """Démarre la partie"""

    def wait(self):
        """Attend que tous les joueurs prévus par l'hôte soient connéctés"""
        self.test_clients()

        if len(self.clients) == 0:
            self.stop()

        time_left = 300
        while len(self.clients) < self.clients_amnt and time_left > 0:
            act_t = time.time()
            stop_time = act_t + 300
            for client in self.clients:
                client.send(str.encode("{\"message\": \"waiting for clients\", \"wait\": \"" + time_left + "\"}"))

            time_left = stop_time - time.time()

        if len(self.clients) == self.clients_amnt:
            self.game_launched = 1
            print(f"Jeu démarré sur serveur {self.id}")
            self.start()

        elif len(self.clients) < self.clients_amnt:
            self.send_all("{\"error\": \"not enough clients\"}")

        else:
            self.send_all("{\"error\": \"too much clients\"}")

        self.stop()

    def stop(self):
        """Arrête le serveur"""
        global SERVERS_LIST
        try:
            self.send_all("{\"message\": \"closing server\"}")
            for adr, _ in self.clients.items():
                self.remove_client(adr)

        finally:
            del SERVERS_LIST[self.id]
            _thread.exit()


def client_thread(client, address):
    """Thread pour la géstion d'un nouveau client"""
    global SERVERS_LIST
    try:
        c.send(str.encode("{\"ask\": \"version\"}"))
        data = c.recv()
        reply = data.decode('utf-8')

        try:
            if not json.loads(reply)["asw"] == GAME_VERSION:
                raise json.decoder.JSONDecodeError

            c.send(str.encode("{\"ask\": \"new or connect\"}"))
            data = c.recv()
            reply = data.decode('utf-8')
            data_j = json.loads(reply)
            if data_j["asw"] == "new":
                server_id = random.randint(1000, 9999)

                while server_id in SERVERS_LIST:
                    server_id = random.randint(1000, 9999)

                SERVERS_LIST[server_id] = Server(server_id, data_j["players"]).add_client(client, address)
                _thread.start_new_thread(SERVERS_LIST[server_id].wait, ())

            elif data_j["asw"] == "connect":
                server_id = data_j["server_id"]
                SERVERS_LIST[server_id].add_client(client, address)

            else:
                raise json.decoder.JSONDecodeError

            while 1:
                action = SERVERS_LIST[server_id].get_action(address)
                if action is not None:
                    pass

        except json.decoder.JSONDecodeError:
            c.send(str.encode("{\"error\": \"invalid answer\"}"))
            c.close()

        except KeyError:
            c.send(str.encode("{\"error\": \"server not found\"}"))
            c.close()


    except socket.error as cl_err:
        print(f"Connexion à {address} fermée : {cl_err}")
        c.close()


s.listen(2)
print("En attente de connexion")

while True:
    c, addr = s.accept()
    print(f"Connecté à : {addr}")
    _thread.start_new_thread(client_thread, (addr, c))
