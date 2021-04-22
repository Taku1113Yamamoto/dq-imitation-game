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




class Map:
    def __init__(self,screen,map_file,player):

        self.map_col = 0 #.mapから読み取った行
        self.map_row = 0 #.mapから読み取った列

        self.screen = screen
        self.player = player

        self.image = load_image("assets/map-images/pipo-map001.png")
        self.umi_image = load_image("assets/map-images/pipo-map001_at-umi.png")
        self.tuti_image = load_image("assets/map-images/pipo-map001_at-tuti.png")
        self.yama2_image = load_image("assets/map-images/pipo-map001_at-yama2.png")
        self.black_image = load_image("assets/map-images/black.png")

        #マップにおく画像を格納
        self.images = []

        #画像内のx,y座標を指定して追加(のちに32をかけてpxに戻す)
        self.images.append([self.umi_image,0,4]) #海0
        self.images.append([self.image,0,0]) #芝生1
        self.images.append([self.image,0,1]) #木2
        self.images.append([self.image,2,1]) #大きな木3
        self.images.append([self.image,7,2]) #洞窟4
        self.images.append([self.image,0,8]) #町5
        self.images.append([self.tuti_image,0,5]) #土6
        self.images.append([self.yama2_image,0,4]) #岩7
        self.images.append([self.black_image,0,0]) #黒8
        self.images.append([self.image,0,6]) #小屋9
        self.images.append([self.image,0,9]) #テント10
        self.images.append([self.image,0,2]) #橋横11
        self.images.append([self.image,1,2]) #橋縦12


        self.map_data = []
        self.readMap(map_file)

        self.map_display = True

    #.mapからマップデータを読み取る,imagesのindex番号でmapを作っていく
    def readMap(self,map_file): 
        with open (map_file) as fi:
            #呼ばれるたびに行が変わる、今回は1行目
            line = fi.readline() 
            line = line.replace("\n","")
            self.map_col, self.map_row = [int(i) for i in line.split(",")] #int型にして取り出す
            for row in range(self.map_row):
                line = fi.readline()
                line = line.replace("\n","")
                self.map_data.append([int(i) for i in line.split(",")])
    
    def drawItems(self,idx,sx,sy,px,py):
        source_image,x,y = self.images[idx]
        #２個目の引数はゲームマップ内の位置、３個目の引数は素材内での位置
        self.screen.blit(source_image,(sx*DOT_SIZE+px,sy*DOT_SIZE+py),(x*DOT_SIZE,y*DOT_SIZE,DOT_SIZE,DOT_SIZE))

    #.mapから読み取った数字の位置にfor文でobjectを配置していく、配置していくものは読み取った数字と一致するimagesのindex番号のもの
    def draw(self,outer):
        px = -self.player.px
        py = -self.player.py

        #playerの位置から計算した描画するべきmapの左上の座標を定義
        #この座標からscreenのcol、row分の範囲を描画していく
        screen_top_left_x = self.player.wx - SCREEN_CENTER_X 
        screen_top_left_y = self.player.wy - SCREEN_CENTER_Y

        for row in range (-1,SCREEN_ROW+1): 
            for col in range (-1,SCREEN_COL+1):
                sx = screen_top_left_x + col
                sy = screen_top_left_y + row

                if not (0 <= sx < self.map_col) or not (0 <= sy < self.map_row):
                    self.drawItems(outer,col,row,px,py)

                else:
                    #背景が透明なobjectをそのままおくと画面の背景が見えてしまうので、下には芝生の画像を敷き詰めておく
                    idx = self.map_data[sy][sx]
                    self.drawItems(1,col,row,px,py)
                    self.drawItems(idx,col,row,px,py)

    def permition(self,sx,sy):
        if not (0 <= sx < self.map_col) or not (0 <= sy < self.map_row):
            return False
        
        idx = self.map_data[sy][sx]
        if idx == 0 or idx == 7 or idx == 8:
            return False
        return True 