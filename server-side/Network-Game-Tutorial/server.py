"""Server module"""
import socket
import random
import json
import _thread
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

class Server:
    def __init__(self, server_id, exp_c_num):
        self.id = server_id
        self.clients = []
        self.todo_action = None
        self.done_actions = []
        self.clients_num = exp_c_num
        self.game_launched = 0

    def add_client(self, client):
        if not self.game_launched:
            self.clients.append(client)
            return self

        return 0

    def test_clients(self):
        counter = 0
        for client in self.clients:
            try:
                client.ping()

            except socket.error:
                self.clients.pop(counter)

            counter += 1

    def stop(self):
        global SERVERS_LIST
        try:
            for client in self.clients:
                client.close()

        finally:
            count = 0
            for serv in SERVERS_LIST:
                if serv.id == self.id:
                    SERVERS_LIST.pop(count)
                    break

                count += 1

    def start(self):
        self.test_clients()

        if len(self.clients) == 0:
            self.stop()

        time_left = 300
        while len(self.clients) < self.clients_num and time_left > 0:
            act_t = time.time()
            stop_time = act_t + 300
            for client in self.clients:
                client.send(str.encode("{\"message\": \"Waiting for clients\", \"wait\": \"" + time_left + "\"}"))

                time_left = stop_time - time.time()

        self.game_launched = 1
        print(f"Jeu démarré sur serveur {self.id}")


SERVERS_LIST = []

s.listen(2)
print("En attente de connexion")

def client_thread(address, client):
    """Client thread"""
    global SERVERS_LIST
    try:
        c.send(str.encode("{\"ask\": \"new or connect\"}"))
        data = c.recv()
        reply = data.decode('utf-8')

        try:
            data_j = json.loads(reply)
            if data_j["asw"] == "new":
                server_id = random.randint(1000, 9999)
                for serv in SERVERS_LIST:
                    if serv.id == server_id:
                        server_id = random.randint(1000, 9999)

                server_num = len(SERVERS_LIST)
                SERVERS_LIST.append(Server(server_id, data_j["players"]).add_client(client))
                _thread.start_new_thread(SERVERS_LIST[server_num].start, (server_id,))

            elif data_j["asw"] == "connect":
                for serv in SERVERS_LIST:
                    if serv.id == data_j["server_id"]:
                        serv.add_client(client)
                        found = 1
                        break

                    found = 0

                if not found:
                    c.send(str.encode("{\"error\": \"server not found\"}"))

        except json.decoder.JSONDecodeError:
            print("Réponse invalide")
            c.close()

    except socket.error as cl_err:
        print(f"Connexion à {address} fermée : {cl_err}")
        c.close()


while True:
    c, addr = s.accept()
    print(f"Connecté à : {addr}")
    _thread.start_new_thread(client_thread, (addr, c,))
