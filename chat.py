import socket
from tkinter import *
from threading import Thread

class ChatClient:
    def __init__(self, master, name, port, server_port, server_ip):
        self.name = name
        self.port = port
        self.server_port = server_port
        self.server_ip = server_ip
        self.buffer = 50
        self.message_field = Entry()
        self.send_button = Button(text="Send")
        self.text = Text()
        self.scrollbar = Scrollbar()
        self.scrollbar.grid(row=0, column=1)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.grid(row=0, column=0)
        self.message_field.grid(row=1, column=0)
        self.send_button.grid(row=2, column=0)
        self.send_button.bind("<Button-1>", self.send_msg)
        master.bind("<Return>", self.send_msg)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((socket.gethostbyname(socket.gethostname()), self.port))
        self.chat_server = (self.server_ip, self.server_port)

        self.file = open("chat.txt", "w")
        self.file.close()
        Thread(target=self.listen_to_msg, args=()).start()
    def send_msg(self, master):
        text = self.name+": "
        text += self.message_field.get()
        self.client.sendto(str(text).encode("utf-8"), self.chat_server)
        self.message_field.destroy()
        self.message_field = Entry()
        self.message_field.grid(row=1, column=0)
    def listen_to_msg(self):
        while True:
            data, addr = self.client.recvfrom(self.buffer)
            data = data.decode("utf-8")
            self.file = open("chat.txt", "a")
            self.file.write(data)
            self.file.write("\n")
            self.file.close()
            self.text.insert(END, data)
            self.text.insert(END, "\n")
class ChatServer:
    def __init__(self, port, player_ports):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.player_ports = player_ports
        self.buffer = 50
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        print("chat started")
    def listen_to_msg(self):
        while True:
            data, addr = self.server.recvfrom(self.buffer)
            if addr in self.player_ports:
                for i in range(0, len(self.player_ports)):
                    self.server.sendto(data, self.player_ports[i])
def start_chat(name, port, server_port, server_ip):
    root = Tk()
    root.title(name)
    CC = ChatClient(root, name, port, server_port, server_ip)
    root.mainloop()
if __name__ == '__main__':
    CS = ChatServer(5005, [("192.168.0.92", 5025)])
    Thread(target=CS.listen_to_msg, args=()).start()
    start_chat("mlody g", 5025, 5005, "192.168.0.92")
