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


class Item():
    def __init__(self):
        self.all_item_list = []
        with open ("assets/item-list.txt") as fi:
            line = fi.readline()
            line = fi.readline()
            line = line.replace("\n","")

            while line:
                self.all_item_list.append([str(i) for i in line.split(",")])
                line = fi.readline()
                line = line.replace("\n","")