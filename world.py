import socket
from generateWorld import GenerateWorld
from threading import Thread
from random import randint
from tkinter import *
from chat import ChatServer
players = []
players_2 = []
players_3 = []
players_4 = []
heroes_status = []
heroes_names = []
class Server:
    def __init__(self, port=None, max_size=None):
        if port==None:
            port = input("Wpisz port: ")
        if max_size == None:
            max_size = input("Wpisz ilosc osob: ")
        self.max_size = max_size
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.box_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.enemies_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), port))
        port += 2
        self.box_server.bind((socket.gethostbyname(socket.gethostname()), port))
        port += 1
        self.enemies_server.bind((socket.gethostbyname(socket.gethostname()), port))
        self.world_gen = GenerateWorld()
        self.heroes_x = []
        self.heroes_y = []
        self.server_heroes_x_y_status = []
        for i in range(0, self.max_size):
            self.heroes_x.append(randint(0, self.world_gen.width-50))
            self.heroes_y.append(randint(0, self.world_gen.height-50))
            self.server_heroes_x_y_status.append(0)
        self.server_heroes_x_y_status = [0, 0, 0, 0]
        self.buffer = 100
        self.boxes_status = []
        self.enemies_amount = randint(20, 80)
        print("SERVER STARTED")
        while len(players)< max_size:
            data, addr = self.server.recvfrom(self.buffer)
            players.append(addr)
            data, addr = self.server.recvfrom(self.buffer)
            players_2.append(addr)
            data, addr = self.server.recvfrom(self.buffer)
            players_3.append(addr)
            data, addr = self.server.recvfrom(self.buffer)
            players_4.append(addr)
            heroes_status.append(0)
            heroes_names.append(data.decode("utf-8"))
        for i in range(0, max_size):
            for j in range(0, max_size):
                self.server.sendto(str(players_2[j]).encode("utf-8"), players[i])
                self.server.sendto(str(heroes_names[j]).encode("utf-8"), players[i])
                self.server.sendto(str(self.heroes_x[j]).encode("utf-8"), players[i])
                self.server.sendto(str(self.heroes_y[j]).encode("utf-8"), players[i])
                self.server.sendto(str(heroes_status[j]).encode("utf-8"), players[i])
                self.server.sendto(str(self.world_gen.width).encode("utf-8"), players[i])
                self.server.sendto(str(self.world_gen.height).encode("utf-8"), players[i])
                self.server.sendto(str(self.world_gen.boxes).encode("utf-8"), players[i])
                self.server.sendto(str(self.enemies_amount).encode("utf-8"), players[i])
        for i in range(0, self.world_gen.boxes):
            x = str(randint(0, self.world_gen.width))
            y = str(randint(0, self.world_gen.height))
            self.boxes_status.append(0)
            for j in range(0, max_size):
                self.server.sendto(x.encode("utf-8"), players[j])
                self.server.sendto(y.encode("utf-8"), players[j])
        for i in range(0, self.enemies_amount):
            x = str(randint(0, self.world_gen.width))
            y = str(randint(0, self.world_gen.height))
            for j in range(0, max_size):
                self.server.sendto(x.encode("utf-8"),players[j])
                self.server.sendto(y.encode("utf-8"), players[j])
    def server_control(self):
        self.action = ""
        for i in range(0, self.max_size):
            Thread(target=self.player_control, args=[i]).start()
            Thread(target=self.handleConnection, args=[i]).start()
        Thread(target=self.handleBox, args=()).start()
        Thread(target=self.handleEnemies, args=()).start()
        while self.action != "q":
            self.action = input("Wpisz komende: ")
            self.choose()
        self.server.close()
    def choose(self):
        if self.action == "show":
            self.showConnection()
        elif self.action == "remove":
            self.remove()
    def remove(self):
        self.numer = input("Ktorego gracza chcesz wyrzucic: ")
        self.numer = int(self.numer)
        self.numer -= 1
        self.server.sendto("q".encode("utf-8"), players[self.numer])
        players.pop(self.numer)
    def player_control(self, number):
        while True:
            for i in range(0, self.max_size):
                if i != number:
                    self.server.sendto(str(self.server_heroes_x_y_status[i]).encode("utf-8"), players[number])
    def showConnection(self):
        for i in range(0, len(players)):
            print("player number {}: {} | name: {}".format(i+1, players[i], heroes_names[i]))

    def handleConnection(self, numer):
        while True:
            data2, addr = self.server.recvfrom(self.buffer)
            if addr == players[numer]:
                data2.decode("utf-8")
                data2 = str(data2)
                self.server_heroes_x_y_status[numer] = data2

    def handleBox(self):
        while True:
            data, addr = self.box_server.recvfrom(self.buffer)
            for i in range(0, self.max_size):
                self.box_server.sendto(data, players_3[i])

    def handleEnemies(self):
        while True:
            data, addr = self.enemies_server.recvfrom(self.buffer)
            if data.decode("utf-8")=="death":
                for i in range(0, self.max_size):
                    if addr == players_3[i]:
                        heroes_status[i] = 1
            else:
                for i in range(0, self.max_size):
                    self.enemies_server.sendto(data, players_3[i])

class FightServer(object):
    def __init__(self, port):
        self.host = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, port))
        self.buffer = 100
        self.max = len(players)
        self.next = 0
    def loop(self):
        while True:
            self.next = 0
            data, addr = self.server.recvfrom(self.buffer)
            data = data.decode("utf-8")
            for i in range(0, self.max):
                if addr == players_2[i]:
                    if heroes_status[i] == 0:
                        self.next = 1
            if self.next == 1:
                if data == "-2":
                    self.start_enemy_fight(addr)
                elif data != "-1" and data != "-3":
                    self.start_fight(addr, data)
    def start_enemy_fight(self, addr):
        player_nr = 0
        for j in range(0, self.max):
            if addr == players_2[j]:
                heroes_status[j] = 3
                player_nr = j

        Thread(target=self.handle_enemy_fight, args=(addr, player_nr)).start()
    def handle_enemy_fight(self, addr2, nr):
        fighting_player_address = addr2
        while True:
            data, addr = self.server.recvfrom(self.buffer)
            if fighting_player_address == addr:
                if data.decode("utf-8") != "-1":
                    heroes_status[nr] = 0
                break
    def start_fight(self, addr, second_address):
        player_2 = second_address
        x = 1
        for j in range(0, self.max):
            if players_2[j] == addr:
                player_1 = j
            if str(players_2[j]) == player_2:
                player_2 = int(j)
                print(j)
                x = 0
        if x:
            print("zajety gracz")
            return 0
        if heroes_status[player_2] != 0:
            print("zajety gracz")
            return 0
        try:
            heroes_status[player_2] = 1
            heroes_status[player_1] = 1
            print(heroes_names[player_1])
            self.server.sendto(str(player_2).encode("utf-8"), players[player_1])
            self.server.sendto(str(player_1).encode("utf-8"), players[player_2])
            Thread(target=self.handle_fight, args=[players_2[player_1], players_2[player_2]]).start()
        except Exception:
            pass
    def handle_fight(self, player_one, player_two):
        self.one = player_one
        self.two = player_two
        print("walka miedzy przeciwnikamioo zaczyna sie")
        while True:
            data, addr = self.server.recvfrom(self.buffer)
            if data.decode("utf-8") == '-1':
                #death of one player
                for j in range(0, self.max):
                    if players_2[j] != addr:
                        if players_2[j] == self.one:
                            heroes_status[j] = 0
                            self.server.sendto(data, self.one)
                            break
                        elif players_2[j] == self.two:
                            heroes_status[j] = 0
                            self.server.sendto(data, self.two)
                            break
            #damge dealing to enemies
            if data.decode("utf-8") == '-1':
                break
            if addr == self.one:
                self.server.sendto(data, self.two)
                self.server.sendto("-2".encode("utf-8"), self.one)
            elif addr == self.two:
                self.server.sendto(data, self.one)
                self.server.sendto("-2".encode("utf-8"), self.two)
class Gui:
    def __init__(self, master):
        self.master = master
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="load settings", command=self.load_settings)
        self.filemenu.add_command(label="save settings", command=self.save_settings)
        self.master.config(menu=self.menubar)
        self.menubar.add_cascade(label="settings", menu=self.filemenu)
        self.server_port = Label(text="SERVER PORT: ")
        self.server_port_field = Entry()
        self.enemies_amount = Label(text="ENEMIES AMOUNT: ")
        self.enemies_amount_field = Entry()
        self.start_server = Button(text="START SERVER")
        self.server_port.grid(row=0, column=0)
        self.server_port_field.grid(row=0, column=1)
        self.enemies_amount.grid(row=1, column=0)
        self.enemies_amount_field.grid(row=1, column=1)
        self.start_server.grid(row=2, columnspan=2)
        self.start_server.bind("<Button-1>", self.start_server_1)
    def save_settings(self):
        f = open("server.txt", "w")
        f.write(self.server_port_field.get())
        f.write("\n")
        f.write(self.enemies_amount_field.get())
    def load_settings(self):
        f=open("server.txt", "r")
        i=0
        for line in f.readlines():
            if i==0:
                self.server_port_field.insert(index=i, string=line)
            if i == 1:
                self.enemies_amount_field.insert(index=i, string=line)
            i+= 1
    def start_server_1(self, master):
        Thread(target=self.start_server_2, args=()).start()
    def start_server_2(self):
        port = int(self.server_port_field.get())
        max = int(self.enemies_amount_field.get())
        S = Server(port, max)
        F = FightServer(port+1)
        CS = ChatServer(port + 5, players_4)
        Thread(target=CS.listen_to_msg, args=()).start()
        Thread(target=F.loop, args=()).start()
        S.server_control()
def main(port, enemies_amount):
    S = Server(port, enemies_amount)
    F = FightServer(port+1)

    Thread(target=F.loop, args=()).start()

    S.server_control()
if __name__ == '__main__':
    root = Tk()
    G = Gui(root)
    root.mainloop()



