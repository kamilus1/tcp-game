import pygame
import socket
from hero import Hero
from bullets import Bullet
from threading import Thread
from generateWorld import GenerateWorld
from time import time
import math
from fight import Skills
from random import randint
from enemy import Enemy
from map import Map
from boxes import Box
from sys import exit
from chat import start_chat
class PlayerWorld:
    def __init__(self, x, y, port, serv_port, host, max_size, name):
        self.width = x
        self.height = y
        self.max_size = max_size
        self.server = (host, serv_port)
        self.fight_server = (host, serv_port+1)
        self.box_server = (host, serv_port+2)
        self.enemies_server = (host, serv_port+3)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((socket.gethostbyname(socket.gethostname()), port))
        port += 1
        self.client_2.bind((socket.gethostbyname(socket.gethostname()), port))
        port += 1
        self.client_3.bind((socket.gethostbyname(socket.gethostname()), port))
        port += 1
        self.client_4.bind((socket.gethostbyname(socket.gethostname()), port))
        self.S = Skills()
        #statistic
        self.dmg = randint(2, 5)
        self.hp = randint(7, 12)
        self.max_hp = self.hp
        self.chance = randint(5, 10)
        self.mp = randint(10, 20)
        self.speed = 5
        self.skills = [self.S.basic, self.S.critic, self.S.heal]
        self.all_skills = [self.S.basic, self.S.critic, self.S.heal, self.S.harnas_vomit, self.S.tatra_shot]
        self.max_lvl = len(self.skills)-2
        self.score = 0
        self.next_skill = 3
        self.colors = []
        for i in range(0, 10):
            self.colors.append((100, 100, 100))
        self.skill_time = 0
        self.stats = False
        pygame.init() #pygame and pygame fonts initialization
        pygame.font.init()
        self.your_hero_x =0
        self.your_hero_y =0
        self.hero_x = []
        self.hero_y = []
        self.hero_status = []
        self.hero_names = []
        self.hero_addresses_all = []
        self.hero_addresses = []
        self.world_w = 0
        self.world_h = 0
        self.boxes = 0
        self.boxes_x = []
        self.boxes_y = []
        self.boxes_status = []
        self.Box = Box()
        self.name = name
        self.buffer = 100
        self.enemy_nr = -2
        self.client.sendto(name.encode("utf-8"), self.server)
        self.client_2.sendto(name.encode("utf-8"), self.server)
        self.client_3.sendto(name.encode("utf-8"), self.server)
        self.client_4.sendto(name.encode("utf-8"), self.server)
        self.client_4.close()
        self.shot_time = time()
        self.red = (200, 50, 50)
        self.blue = (60, 90, 220)
        self.green = (40, 220, 80)
        # local enemies init
        self.enemies = []
        self.enemies_x = []
        self.enemies_y = []
        self.enemies_status = []
        self.local_enemy_nr = -2
        #getting variables values from server
        for j in range(0, max_size):
            self.data, addr = self.client.recvfrom(self.buffer)
            self.hero_addresses_all.append(self.data.decode("utf-8"))
            self.hero_addresses.append(self.data.decode("utf-8"))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.hero_names.append(self.data.decode("utf-8"))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.hero_x.append(int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.hero_y.append(int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.hero_status.append(int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.world_w = (int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.world_h = (int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.boxes = (int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.enemies_amount = int(self.data.decode("utf-8"))
        for i in range(0, self.boxes):
            self.data, addr = self.client.recvfrom(self.buffer)
            self.boxes_x.append(int(self.data.decode("utf-8")))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.boxes_y.append(int(self.data.decode("utf-8")))
            self.boxes_status.append(0)
        for i in range(0, self.enemies_amount):
            self.data, addr = self.client.recvfrom(self.buffer)
            self.enemies_x.append(int(self.data))
            self.data, addr = self.client.recvfrom(self.buffer)
            self.enemies_y.append(int(self.data))
        self.screen = pygame.display.set_mode((self.width, self.height))
        for i in range(0, self.enemies_amount):
            self.enemies.append(Enemy(self.red, self.screen))
            self.enemies_status.append(0)
        self.real_boxes_x = self.boxes_x
        self.real_boxes_y = self.boxes_y
        for i in range(0, self.max_size):
            if self.hero_names[i] == name:
                self.your_hero_x = self.hero_x[i]
                self.your_hero_y = self.hero_y[i]
                self.hero_x.pop(i)
                self.hero_y.pop(i)
                self.hero_addresses.pop(i)
                self.hero_status.pop(i)
                self.hero_names.pop(i)
                self.max_size-=1
                break
        for i in range(0, self.max_size):
            print(self.hero_names[i])
            print(self.hero_addresses[i])
            print(self.hero_x[i])
            print(self.hero_y[i])
        #worrld and map gen
        self.worldGen = GenerateWorld(self.world_w, self.world_h, self.boxes ,self.boxes_x, self.boxes_y)
        self.map = Map(self.screen, self.world_w, self.world_h, self.boxes_x, self.boxes_y, self.enemies_x, self.enemies_y)
        self.bool_map = False
        self.buttle_x = - 100000
        self.buttle_y = - 100000

        self.clock = pygame.time.Clock()
        #heroes init
        self.hero = Hero((160, 32, 240  ), self.screen)
        self.heroes = []
        self.name = name
        self.xp = 0
        self.lvl_xp = 100
        self.lvl = 1
        print(self.name)
        for i in range(0, self.max_size):
            self.heroes.append(Hero((255, 0, 0), self.screen))
        self.speed_x = 0
        self.speed_y = 0
        self.status = 0
        self.player_x = (x/2)-25
        self.player_y = (y/2)-25
        #rendering "harnas" beer
        self.image = pygame.image.load("harnas1.png")
        self.screen.blit(self.image, (500, 250))
        self.buck = Bullet(self.screen)
        self.pos_x = 0
        self.pos_y = 0
        self.turn = 2
        self.first_or_second = 2
        self.shot_or_not_shot = False
        self.timer = time()
        self.wait_time = 0
    def wait_loop(self):
        while self.wait_time>=0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    exit()
            self.screen.fill((0, 0, 0))
            if time() - self.timer>=1:
                self.wait_time-=1
                self.timer = time()
            self.font_config(100, self.width/2, self.height/2, (255, 255, 255), "{}".format(self.wait_time), True)
            pygame.display.flip()
            self.clock.tick(60)
    def game_loop(self):
        Thread(target=self.handleConnection, args=()).start()
        Thread(target=self.sendPosition, args=()).start()
        Thread(target=self.boxEnemiesStatus, args=()).start()

        self.wait_loop()
        while True:
            while self.status == 0:
                self.screen.fill((0, 0, 0))
                self.eventLoop()
                self.worldGen.drawWorld(self.screen, self.player_x-self.your_hero_x, self.player_y-self.your_hero_y, (50, 150, 10))
                self.drawBoxes()
                self.hero.display(self.player_x, self.player_y, self.name)
                self.showEnemies()
                self.showHeroes()
                self.mapLeft()
                self.experience()
                self.choose()
                self.your_hero_x += self.speed_x
                self.your_hero_y += self.speed_y
                self.buttle_x, self.buttle_y, self.shot_or_not_shot = self.buck.display(self.buttle_x, self.buttle_y, self.width/2-15, self.height/2-25, self.shot_or_not_shot)
                self.font_config(30, 900, 10, self.red, "HP: {}".format(self.hp))
                self.font_config(30, 80, 10, (255, 225, 0), "SCORE: {}".format(self.score))
                self.additionDisplay()
                pygame.display.flip()
                self.clock.tick(60)
            while self.status == 1:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pass
                        if self.turn % 2 == self.first_or_second:
                            if event.key == pygame.K_1:
                                self.colors[0] = (255, 255, 255)
                            if event.key == pygame.K_2:
                                if self.mp > 1:
                                    self.colors[1] = (255, 255, 255)
                            if event.key == pygame.K_3:
                                self.colors[2] = (255, 255, 255)
                            if event.key == pygame.K_4:
                                self.colors[3] = (255, 255, 255)
                            if event.key == pygame.K_5:
                                self.colors[4] = (255, 255, 255)
                    if event.type == pygame.KEYUP:
                        if self.turn % 2 == self.first_or_second:
                            if event.key == pygame.K_1:
                                self.colors[0] = (100, 100, 100)
                                self.skills[0](self.dmg, self.fight_server, self.client_2)
                            if event.key == pygame.K_2:
                                if self.mp > 1:
                                    self.colors[1] = (100, 100, 100)
                                    self.mp = self.skills[1](self.dmg, self.chance,self.mp, self.fight_server, self.client_2)
                            if event.key == pygame.K_3:
                                self.colors[2] = (100, 100, 100)
                                self.hp, self.mp = self.skills[2](self.hp, self.max_hp, self.mp, self.client_2, self.fight_server)
                            if event.key == pygame.K_4:
                                self.colors[3] = (100, 100, 100)
                                if self.next_skill >3:
                                    self.hp= self.skills[3](self.dmg, self.hp, self.client_2, self.fight_server)
                self.screen.fill((20, 30, 150))
                self.hero.display(self.width/6, self.height/1.4, self.name)
                self.heroes[self.enemy_nr].display(self.width/1.4, self.height/6, "!")
                self.font_config(50, self.width / 2, 100, (150, 30, 50), "HP:{}".format(self.hp), True)
                self.skills_display()
                if self.turn %2 == self.first_or_second:
                    self.font_config(30, 700, 500, self.green, "YOUR TURN")
                else:
                    self.font_config(30, 700, 500, self.red, "ENEMY TURN")
                if self.hp < 0:
                    self.status = 3
                    while 1:
                        self.client_2.sendto("-1".encode("utf-8"), self.fight_server)
                        if time() - c >2:
                            pygame.quit()
                            quit()
                            break
                else:
                    c = time()
                pygame.display.flip()
                self.clock.tick(60)
            while self.status == 2:
                deal_dmg = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if self.turn %2 == self.first_or_second:
                            if event.key == pygame.K_1:
                                self.colors[0] = (255, 255, 255)
                            if event.key == pygame.K_2:
                                self.colors[1] = (255, 255, 255)
                            if event.key == pygame.K_3:
                                self.colors[2] = (255, 255, 255)
                            if event.key == pygame.K_4:
                                self.colors[3] = (255, 255, 255)
                    if event.type == pygame.KEYUP:
                        if self.turn%2 == self.first_or_second:
                            if event.key == pygame.K_1:
                                self.colors[0] = (100, 100, 100)
                                deal_dmg = self.skills[0](self.dmg)
                                self.enemies[self.local_enemy_nr].get_shot(deal_dmg)
                                self.turn += 1
                            if event.key == pygame.K_2:
                                if self.mp > 1:
                                    self.colors[1] = (100, 100, 100)
                                    deal_dmg, self.mp = self.skills[1](self.dmg, self.chance, self.mp)
                                    self.enemies[self.local_enemy_nr].get_shot(deal_dmg)
                                    self.turn += 1
                            if event.key == pygame.K_3:
                                self.colors[2] = (100, 100, 100)
                                self.hp, self.mp = self.skills[2](self.hp, self.max_hp, self.mp)
                                self.turn += 1
                            if event.key == pygame.K_4:
                                self.colors[3] = (100, 100, 100)
                                if self.next_skill > 3:
                                    deal_dmg, self.hp = self.skills[3](self.hp, self.dmg)
                                    self.enemies[self.local_enemy_nr].get_shot(deal_dmg)
                                    self.turn +=1
                if self.hp < 0:
                    self.status = 3
                    while 1:
                        self.client_2.sendto("-1".encode("utf-8"), self.fight_server)
                        if time() - c >2:
                            pygame.quit()
                            quit()
                            break
                else:
                    c = time()
                if self.enemies[self.local_enemy_nr].hp < 0:
                    self.client_3.sendto(str(self.local_enemy_nr).encode("utf-8"), self.enemies_server)
                    self.xp += 50
                    self.score += 20
                    while 1:
                        self.client_2.sendto("-3".encode("utf-8"), self.fight_server)
                        if time() - s > 2:
                            self.status = 0
                            break

                    self.turn+=1
                else:
                    s = time()
                if self.turn %2 == self.first_or_second:
                    self.font_config(30, 700, 500, self.green, "YOUR TURN")
                else:
                    self.hp = self.enemies[self.local_enemy_nr].attack(self.hp)
                    self.turn += 1
                self.screen.fill((20, 30, 150))
                self.hero.display(self.width / 6, self.height / 1.4, self.name)
                self.enemies[self.local_enemy_nr].display(self.width/1.4, self.height/6)
                self.font_config(50, self.width/2, 100, self.red, "HP:{}".format(self.hp), True)
                self.skills_display()
                pygame.display.flip()
                self.clock.tick(60)
            self.turn = 2
            self.first_or_second = 2
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.speed_y = -1*self.speed
                elif event.key == pygame.K_s:
                    self.speed_y = 1*self.speed
                if event.key == pygame.K_a:
                    self.speed_x = -1*self.speed
                elif event.key == pygame.K_d:
                    self.speed_x = 1*self.speed
                if event.key == pygame.K_ESCAPE:
                    self.bool_map = True
                if event.key == pygame.K_TAB:
                    self.stats = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.speed_y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.speed_x = 0
                if event.key == pygame.K_ESCAPE:
                    self.bool_map = False
                if event.key == pygame.K_TAB:
                    self.stats = False
    def sendPosition(self):
        while True:
                self.text = str(self.your_hero_x) + ";"
                self.text += str(self.your_hero_y)
                self.text += ";"
                self.text += str(self.status)
                self.text += ";"
                self.text += str(self.name)
                self.text += ";"
                self.client.sendto(str(self.text).encode("utf-8"), self.server)
    def listenToFight(self, name):
        self.enemy_nr = int(name)
        if self.enemy_nr == self.max_size:
            self.enemy_nr -= 1
        self.status = 1
        while self.status == 1:
            data, addr = self.client_2.recvfrom(self.buffer)
            data = data.decode("utf-8")
            if data == "-1":
                self.status = 0
                self.xp += 60
                self.score += 40
                self.turn = 2
                self.first_or_second = 2
            elif data == "-2":
                self.turn += 1
            else:
                self.turn += 1
                data = int(data)
                self.hp -= data
    def handleConnection(self):
        while True:
                data3, addr = self.client.recvfrom(self.buffer)
                if self.status == 0 and addr == self.fight_server:
                    print(data3.decode("utf-8"))
                    if self.first_or_second == 2:
                        self.first_or_second = 1
                    Thread(target=self.listenToFight, args=[data3.decode("utf-8")]).start()
                else:
                    data3 = data3.decode("utf-8")
                    data3 = str(data3)
                    i = 2
                    pos_x = ""
                    pos_y = ""
                    status = ""
                    name = ""
                    try:
                        while data3[i] != ";":
                            pos_x += data3[i]
                            i+=1
                        i += 1
                        while data3[i] != ";":
                            pos_y += data3[i]
                            i += 1
                        i+=1
                        status = data3[i]
                        i += 2
                        while data3[i] != ";":
                            name += data3[i]
                            i += 1

                    except Exception:
                        pass
                    try:
                        for j in range(0, self.max_size):
                            if self.hero_names[j] == str(name):
                                self.hero_x[j] = int(pos_x)
                                self.hero_y[j] = int(pos_y)
                                self.hero_status[j] = int(status)

                                break
                    except Exception:
                        pass
    def showEnemies(self):
        radius = 30
        for i in range(0, self.enemies_amount):
            if self.enemies_status[i] == 0:
                enemy_x = self.enemies_x[i] - self.your_hero_x
                enemy_y = self.enemies_y[i] - self.your_hero_y
                enemy_x += self.player_x
                enemy_y += self.player_y
                self.enemies[i].display(enemy_x, enemy_y)
                range_x = (enemy_x + 25) - self.buttle_x
                range_y = (enemy_y + 25) - self.buttle_y
                distance = range_x * range_x
                distance += range_y * range_y
                distance = math.sqrt(distance)
                if distance < 2 * radius and time() - self.shot_time > 2:
                    self.shot_or_not_shot = False
                    self.buttle_x = -100000
                    self.buttle_y = -100000
                    self.client_2.sendto("-2".encode("utf-8"), self.fight_server)
                    self.local_enemy_nr = i
                    self.first_or_second = 0
                    self.status = 2
                    self.shot_time = time()
    def showHeroes(self):
        radius = 30
        for i in range(0, self.max_size):
            if self.hero_status[i] == 0:
                pos_x = self.hero_x[i] - self.your_hero_x
                pos_y = self.hero_y[i] - self.your_hero_y
                pos_x += self.player_x
                pos_y += self.player_y
                self.heroes[i].display(pos_x, pos_y, self.hero_names[i])
                range_x = (pos_x+25) - self.buttle_x
                range_y = (pos_y+25) - self.buttle_y
                distance = range_x*range_x
                distance += range_y*range_y
                distance = math.sqrt(distance)
                if distance < 2*radius and time()-self.shot_time > 2:
                    self.shot_or_not_shot = False
                    self.buttle_x = -100000
                    self.buttle_y = -100000
                    self.first_or_second = 0
                    self.client_2.sendto(str(self.hero_addresses[i]).encode("utf-8"), self.fight_server)
                    self.shot_time = time()
    def skills_display(self):
        for i in range(0, len(self.skills)):
            pygame.draw.rect(self.screen, self.colors[i], (10+i*1004/len(self.skills)+2*i, 640, 1004/len(self.skills), 50))
    def font_config(self, size, x, y, color, text, center=None):
        myfont = pygame.font.SysFont("Comic Sans MS", size)
        textsurface = myfont.render(text, True, color)
        if center:
            self.screen.blit(textsurface, (x-textsurface.get_width(), y-textsurface.get_height()))
        else:
            self.screen.blit(textsurface, (x, y))
    def boxEnemiesStatus(self):
        while True:
                data, addr = self.client_3.recvfrom(self.buffer)
                data = data.decode("utf-8")
                data = int(data)
                if addr == self.box_server:
                    self.boxes_status[data] = 1
                elif addr == self.enemies_server:
                    self.enemies_status[data] = 1
    def drawBoxes(self):
        for i in range(0, self.boxes):
            if self.boxes_status[i] == 0:
                pos_x = self.boxes_x[i] - self.your_hero_x
                pos_y = self.boxes_y[i] - self.your_hero_y
                pos_x += self.player_x
                pos_y += self.player_y
                self.Box.showBox(self.screen, pos_x, pos_y)
                if self.player_x > pos_x and self.player_x <pos_x+50 or self.player_x<pos_x and self.player_x+50>pos_x:
                    if self.player_y >pos_y and self.player_y <pos_y + 50 or self.player_y<pos_y and self.player_y+50> pos_y:
                            self.client_3.sendto(str(i).encode("utf-8"), self.box_server)
                            self.hp, self.dmg, self.speed, self.mp, self.xp, self.chance = self.Box.effect(self.hp, self.dmg, self.speed, self.mp, self.xp, self.lvl, self.chance)
    def mapLeft(self):
        if self.your_hero_x+50<0 or self.your_hero_x > self.world_w:
            self.client_3.sendto("death".encode("utf-8"), self.enemies_server)
            self.status = 3
            pygame.quit()
            quit()
        elif self.your_hero_y+50 < 0 or self.your_hero_y > self.world_h:
            self.client_3.sendto("death".encode("utf-8"), self.enemies_server)
            self.status = 3
            pygame.quit()
            quit()
    def showStatistics(self):
        self.font_config(30, self.width/2, 100, (255, 255, 255), "DMG: {}".format(self.dmg), True)
        self.font_config(30, self.width/2, 150, (255, 255, 255), "HP: {}".format(self.hp), True)
        self.font_config(30, self.width/2, 200, (255, 255, 255), "SPEED: {}".format(self.speed), True)
        self.font_config(30, self.width/2, 250, (255, 255, 255), "MANA: {}".format(self.mp), True)
        self.font_config(30, self.width/2, 300, (255, 255, 255), "LVL: {}".format(self.lvl), True)
        self.font_config(30, self.width/2, 350, (255, 255, 255), "LUCK: {}".format(self.chance), True)
    def additionDisplay(self):
        if self.bool_map:
            self.map.display(self.your_hero_x, self.your_hero_y)
        elif self.stats:
            self.showStatistics()
    def experience(self):
        scale = 200/self.lvl_xp
        pygame.draw.rect(self.screen, (255, 255, 255), ((self.width/2)-100, 20, 200, 25))
        pygame.draw.rect(self.screen, (125, 255, 212), ((self.width/2)-100, 20, self.xp*scale, 25))
        if self.xp >= self.lvl_xp:
            self.xp -= self.lvl_xp
            self.lvl += 1
            self.lvl_xp *= 2
            self.skill_time = time()
    def choose(self):
        if time() - self.skill_time < 5:
                x1 = 300
                x2 = 600
                y1 = 400
                w = 100
                h = 100
                red = self.red
                green = self.green
                if pygame.mouse.get_pos()[0] > x1 and pygame.mouse.get_pos()[0] < x1+w:
                    if pygame.mouse.get_pos()[1] > y1 and pygame.mouse.get_pos()[1]<y1+h:
                        red = (200, 200, 200)
                        if pygame.mouse.get_pressed()[2]:
                            i = randint(0, 2)
                            if i==0:
                                self.max_hp += 1*self.lvl
                                self.hp = self.max_hp
                            elif i== 1:
                                self.dmg += 1*self.lvl
                            elif i ==2:
                                self.mp += 2*self.lvl
                            self.skill_time = 0
                if pygame.mouse.get_pos()[0] > x2 and pygame.mouse.get_pos()[0] < x2+w:
                    if pygame.mouse.get_pos()[1] > y1 and pygame.mouse.get_pos()[1]<y1+h:
                        green = (200, 200, 200)
                        if pygame.mouse.get_pressed()[2]:
                            self.skills.append(self.all_skills[self.next_skill])
                            self.colors.append((100, 100, 100))
                            self.next_skill += 1
                            self.skill_time = 0
                pygame.draw.rect(self.screen, red, (x1, y1, w, h))
                self.font_config(50, x1, y1, (255, 255, 255), "1", True)
                pygame.draw.rect(self.screen, green, (x2, y1, w, h))
                self.font_config(50, x2, y1, (255, 255, 255), "2", True)
if __name__ == '__main__':
    f = open("player.txt", "r+")
    tab = []
    for line in f.readlines():
        tab.append(line)
    f.close()
    port = 5025 #write player port here
    server_port = 5000 #write server port here
    ip = "192.168.0.92" #write server ip here
    player_amount = 2 #write player amount here
    name = "mlody_paranoja" #write player name here
    Player = PlayerWorld(1024, 700, port, server_port, ip, player_amount, name)
    Thread(target=Player.game_loop, args=()).start()
    start_chat(name, port+3, server_port+5, ip)
