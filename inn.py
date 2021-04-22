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





class Inn():
    def __init__(self,menu,player,screen,item):
        self.menu = menu
        self.player = player
        self.screen = screen
        self.inn_display = False
        self.inn_select_num = 0
        self.count = 0
    
    def update(self,x,y):
        if(self.player.wx == x and self.player.wy == y):
            self.inn_display = True
    
    def innAnim(self):
        self.count += 1
        self.menu.drawStaGol()
        drawText(self.screen,"たびびとのやどやに　ようこそ！　","ひとばん　10ゴールドになりますが","おとまりに　なりますか？","")
        
        self.inn_list = ["とまる","やめる"]
        pygame.draw.rect(self.screen,BLACK,Rect(20,20,200,140))
        pygame.draw.rect(self.screen,WHITE,Rect(20,20,200,140),5)
        for i in range (len(self.inn_list)):
            drawChar(self.screen,self.inn_list[i],60,20+i*40)
        self.drawTri(40,39+self.inn_select_num*40,self.count)
    
    def drawTri(self,x,y,count):
        if(count%80 >30):
            pygame.draw.polygon(self.screen,WHITE,[(x,y+20),(x+13,y+10),(x,y)])
        else:
            pygame.draw.polygon(self.screen,BLACK,[(x,y+20),(x+13,y+10),(x,y)])
         