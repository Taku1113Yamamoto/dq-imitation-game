import pygame
import sys
import random
from pygame.locals import *

import mojimoji as moji



#rectで指定
SCREEN_RECT = Rect(0, 0, 640, 480)

#キャラ画像サイズ
IMAGE_SIZE = 32

#スクリーンの要素の大きさ
DOT_SIZE = 32

SCREEN_COL = SCREEN_RECT.width//DOT_SIZE
SCREEN_ROW = SCREEN_RECT.height//DOT_SIZE
SCREEN_CENTER_X = SCREEN_RECT.width//2//DOT_SIZE
SCREEN_CENTER_Y = SCREEN_RECT.height//2//DOT_SIZE

PLAYER_FRONT = 0
PLAYER_LEFT = 1
PLAYER_RIGHT = 2
PLAYER_BACK = 3

ANIM_WAIT_COUNT = 16

MOVE_VELOCITY = 4

FONT_PATH = "assets/DragonQuestFC.ttf"
LINE_WIDTH = 5
FONT_SIZE = 40
WHITE = (255,255,255)
BLACK = (0,0,0)



#画像読み込み
def load_image(file_image):
    image = pygame.image.load(file_image)
    image = image.convert_alpha() #透明とかを変換してくれる
    return image

#32*32に分割して画像の(x,y)の位置を表示
def divide_image(load_image,x,y,width,hight):
    image = pygame.Surface([width,hight])
    image.blit(load_image,(0,0),(x,y,width,hight))
    image = image.convert_alpha()
    return image


def drawText(screen,text1,text2,text3,text4):
    pygame.draw.rect(screen,BLACK,Rect(70,280,500,180))
    pygame.draw.rect(screen,WHITE,Rect(70,280,500,180),5)
    drawChar(screen,moji.han_to_zen(text1),90,290)
    drawChar(screen,moji.han_to_zen(text2),90,323)
    drawChar(screen,moji.han_to_zen(text3),90,356)
    drawChar(screen,moji.han_to_zen(text4),90,389)

def drawChar(screen,char,x,y):
    text_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    text = text_font.render(char,False,WHITE)
    screen.blit(text,(x,y))



class Player (pygame.sprite.Sprite):
    def __init__(self,file_image,title,item):
        pygame.sprite.Sprite.__init__(self)
        self.title = title
        self.item = item

        #player画像を読み込み
        loaded_image = load_image(file_image)

        #前、左、右、後ろ向きに分けて格納する
        self.images = [[],[],[],[]] 

        #imagesに0->1->2->1->0の順に画像が回っていくように格納
        for i in range(0,4):
            for j in [0,1,2,1]:
                self.images[i].append(divide_image(loaded_image,IMAGE_SIZE*j,IMAGE_SIZE*i,IMAGE_SIZE,IMAGE_SIZE)) 
        self.image = self.images[PLAYER_FRONT][0]

        #中心に持ってくる
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_RECT.width/2,SCREEN_RECT.height/2)

        #正確な中心だとマップの角が中心になるので少し動かす 
        self.rect.x = SCREEN_CENTER_X * DOT_SIZE
        self.rect.y = SCREEN_CENTER_Y * DOT_SIZE

        self.frame = 0
        self.anim_count = 0

        #playerの向きを定義、向きはグローバル変数にて定義
        self.dir = PLAYER_FRONT

        #playerの初期位置を定義(mapに対して)
        self.wx, self.wy = 16, 4

        self.moving = False
        self.moving_wait =True
        self.move_count = 0
        self.vx, self.vy = 0, 0
        self.px, self.py = 0, 0
        self.where = 0

        self.exp = 0
        self.gold = 0
        self.saved_player_data = ""

        self.item1 = 0
        self.item2 = 0
        self.item3 = 0
        self.item4 = 0
        self.item5 = 0
        self.item_nums = []
        self.item_list = []

        self.itemSet(self.item)


        self.lv_tables = []
        self.readTable()

        self.all_magic_list = []
        with open ("assets/magic-list.txt") as fi:
            line = fi.readline()
            line = fi.readline()
            line = line.replace("\n","")
            while line:
                self.all_magic_list.append([str(i) for i in line.split(",")])
                line = fi.readline()
                line = line.replace("\n","")


        self.lv = 1
        self.max_hp = 15
        self.max_mp = 7
        self.attack = 7
        self.defence = 7
        self.magic_list_num = []
        self.magic_list = []


        self.selected_magic = "メラ"
        self.selected_magic_damage = 0
        self.selected_magic_mp = 0
        self.selected_magic_heal = 0
    
    def itemSet(self,item):
        for i in range (len(self.item_nums)):
            if not self.item_nums[i] == 0:
                self.item_list.append(item.all_item_list[self.item_nums[i]-1])

    def mapSet(self,load_map):
        self.map = load_map

    def readTable(self):
        with open ("assets/lv-tables.txt") as fi:
            line = fi.readline()
            line = fi.readline()
            line = line.replace("\n","")
            while line:
                self.lv_tables.append([int(i) for i in line.split(",")])
                line = fi.readline()

    

    def parameterSet(self):
        with open ("assets/saved-player-data.txt") as fi:
            line = fi.readline()
            self.saved_player_data += line
            line = fi.readline()
            self.saved_player_data += line
            line = line.replace("\n","")
            if(self.title.title_select_num == 1):
                self.hp,self.mp,self.exp,self.gold,self.wx,self.wy,self.where,self.item1,self.item2,self.item3,self.item4,self.item5 = [int(i) for i in line.split(",")]
            line = fi.readline()
            line = line.replace("\n","")
            if(self.title.title_select_num == 0):
                self.hp,self.mp,self.exp,self.gold,self.wx,self.wy,self.where,self.item1,self.item2,self.item3,self.item4,self.item5 = [int(i) for i in line.split(",")]
            self.item_nums.append(self.item1)
            self.item_nums.append(self.item2)
            self.item_nums.append(self.item3)
            self.item_nums.append(self.item4)
            self.item_nums.append(self.item5)

        for i in range (len(self.lv_tables)):
            if not i == len(self.lv_tables)-1:
                if(self.lv_tables[i][5] <= self.exp):
                    if not self.lv_tables[i][6] == 0:
                        self.magic_list_num.append(self.lv_tables[i][6])
                if(self.lv_tables[i][5] <= self.exp < self.lv_tables[i+1][5]):
                    self.lv = self.lv_tables[i][0]
                    self.max_hp = self.lv_tables[i][1]
                    self.max_mp = self.lv_tables[i][2]
                    self.attack = self.lv_tables[i][3]
                    self.defence = self.lv_tables[i][4]
            else:
                if(self.lv_tables[i][5] <= self.exp):
                    if not self.lv_tables[i][6] == 0:
                        self.magic_list_num.append(self.lv_tables[i][6])
                    self.lv = self.lv_tables[i][0]
                    self.max_hp = self.lv_tables[i][1]
                    self.max_mp = self.lv_tables[i][2]
                    self.attack = self.lv_tables[i][3]
                    self.defence = self.lv_tables[i][4]

            
            


    def keyEvents(self,menu_display):
        if self.moving_wait and not menu_display:
            if self.moving:
                self.px += self.vx
                self.py += self.vy
                if self.px % DOT_SIZE == 0 and self.py % DOT_SIZE == 0:
                    self.moving = False
                    self.wx += self.px // DOT_SIZE
                    self.wy += self.py // DOT_SIZE
                    self.vx, self.vy = 0, 0
                    self.px, self.py = 0, 0
                    self.move_count += 1
            else:
                self.pressed_keys = pygame.key.get_pressed()
                if self.pressed_keys[K_DOWN]:
                    self.dir = PLAYER_FRONT
                    if self.map.permition(self.wx, self.wy + 1):
                        self.moving = True
                        self.vy = MOVE_VELOCITY
                elif self.pressed_keys[K_LEFT]:
                    self.dir = PLAYER_LEFT
                    if self.map.permition(self.wx - 1, self.wy):
                        self.moving = True
                        self.vx = -MOVE_VELOCITY
                elif self.pressed_keys[K_RIGHT]:
                    self.dir = PLAYER_RIGHT
                    if self.map.permition(self.wx + 1, self.wy):
                        self.moving = True
                        self.vx = MOVE_VELOCITY
                elif self.pressed_keys[K_UP]:
                    self.dir = PLAYER_BACK
                    if self.map.permition(self.wx, self.wy - 1):
                        self.moving = True
                        self.vy = -MOVE_VELOCITY

    #画像をループ再生、anim_count分待ってから画像を変えることでframeRateをあげても画像がゆっくり変わる
    def update(self,menu_display):
        self.menu_display = menu_display
        self.keyEvents(self.menu_display)
        self.anim_count += 1
        if self.anim_count >= ANIM_WAIT_COUNT: #24カウントたったら画像を変更
            self.anim_count = 0
            self.frame += 1
        if self.frame > 3:
            self.frame = 0
        self.image = self.images[self.dir][self.frame]