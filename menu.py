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








class Menu():
    def __init__(self,screen,player):
        self.player = player
        self.screen = screen
        self.count = 0
        self.menu_display = False 
        self.menu_select_num = 0
        self.show_statas = False
        self.show_items = False 
        self.show_magics = False
        self.item_select_num = 0
        self.item_select_tri = False
        self.use_item = []
        self.use_item_anim = False
        self.magic_arrow_num = 0
        self.magic_arrow_max_num = 0
        self.magic_arrow_num_correct = 0
        self.magic_select_tri = False
        self.use_magic_anim = False

    
    def update(self):
        self.count += 1
        pygame.draw.rect(self.screen,BLACK,Rect(50,20,140,140))
        pygame.draw.rect(self.screen,WHITE,Rect(50,20,140,140),5)
        commands = ["つよさ","どうぐ","じゅもん"]
        statas_list = ["ＬＶ　　　：","ＨＰ　　　：","ＭＰ　　　：","ちから　　：","みのまもり：","ＥＸ　　　："]
        statas_player_list =[self.player.lv,self.player.hp,self.player.mp,self.player.attack,self.player.defence,self.player.exp]
        for i in range (len(commands)):
            drawChar(self.screen,commands[i],80,20+i*40) 
        
       
        self.drawStaGol()

        self.drawTri(60,39+self.menu_select_num*40,self.count)
        if self.show_statas:
            self.menu_select_num = 0
            pygame.draw.rect(self.screen,BLACK,Rect(200,20,255,250))
            pygame.draw.rect(self.screen,WHITE,Rect(200,20,255,250),5)
            for i in range (len(statas_list)):
                drawChar(self.screen,statas_list[i],220,20+i*40)
            for j in range(len(statas_player_list)):
                drawChar(self.screen,moji.han_to_zen(str(statas_player_list[j])),340,20+j*40)
        if self.show_items:
            self.menu_select_num = 1
            self.drawItems()
        if self.item_select_tri:
            self.drawTri(215,37+self.item_select_num*40,self.count)
        if self.use_item_anim:
            drawText(self.screen,"ゆうしゃは　"+moji.han_to_zen(str(self.use_item[1]))+"を　つかった！","ゆうしゃの　キズが　かいふくした！","","")
        if self.show_magics:
            self.menu_select_num = 2
            pygame.draw.rect(self.screen,BLACK,Rect(200,20,160,180))
            pygame.draw.rect(self.screen,WHITE,Rect(200,20,160,180),5)
            magic_count = len(self.player.magic_list)
            if magic_count<4:
                for i in range (magic_count):
                    drawChar(self.screen,self.player.magic_list[i][1],242,28+37*i)
            else:
                for i in range (4):
                    if(self.magic_arrow_num<4):
                        drawChar(self.screen,self.player.magic_list[i][1],242,28+37*i)
                    else:
                        drawChar(self.screen,self.player.magic_list[self.magic_arrow_num-3+i][1],242,28+37*i)
        if self.magic_select_tri:
            self.magic_arrow_max_num = len(self.player.magic_list)-1
            if(self.magic_arrow_num >3):
                self.magic_arrow_num_correct = 3
            else:
                self.magic_arrow_num_correct = self.magic_arrow_num
            self.drawTri(215,48+self.magic_arrow_num_correct*37,self.count)
            self.player.selected_magic = self.player.magic_list[self.magic_arrow_num][1]
            self.player.selected_magic_mp = int(self.player.magic_list[self.magic_arrow_num][2])
            self.player.selected_magic_damage = int(self.player.magic_list[self.magic_arrow_num][3])
            self.player.selected_magic_heal = int(self.player.magic_list[self.magic_arrow_num][4])
        if self.use_magic_anim:
            drawText(self.screen,"ゆうしゃは　"+moji.han_to_zen(str(self.player.selected_magic))+"を　となえた！","ゆうしゃの　キズが　かいふくした！","","")

    def drawTri(self,x,y,count):
        if(count%80 >30):
            pygame.draw.polygon(self.screen,WHITE,[(x,y+20),(x+13,y+10),(x,y)])
        else:
            pygame.draw.polygon(self.screen,BLACK,[(x,y+20),(x+13,y+10),(x,y)])
    
    def drawItems(self):
        pygame.draw.rect(self.screen,BLACK,Rect(200,20,180,215))
        pygame.draw.rect(self.screen,WHITE,Rect(200,20,180,215),5)
        for i in range (len(self.player.item_list)):
            drawChar(self.screen,moji.han_to_zen(self.player.item_list[i][1]),240,20+i*40)
    
    def drawStaGol(self):
        
        pygame.draw.rect(self.screen,BLACK,Rect(440,20,160,120))
        pygame.draw.rect(self.screen,WHITE,Rect(440,20,160,120),5)
        pygame.draw.rect(self.screen,BLACK,Rect(480,15,80,10))
        drawChar(self.screen,"ゆうしゃ",482,-8)
        drawChar(self.screen,"Ｈ　" + moji.han_to_zen(str(self.player.hp)),482,23)
        drawChar(self.screen,"Ｍ　" + moji.han_to_zen(str(self.player.mp)),482,55)
        if(self.player.lv <10):
            drawChar(self.screen,"ゆ：　" + moji.han_to_zen(str(self.player.lv)),482,87)
        else:
            drawChar(self.screen,"ゆ：" + moji.han_to_zen(str(self.player.lv)),482,87)
        pygame.draw.rect(self.screen,BLACK,Rect(460,145,140,40))
        pygame.draw.rect(self.screen,WHITE,Rect(460,145,140,40),5)
        
        
        drawChar(self.screen,moji.han_to_zen(str(self.player.gold)+"G"),480,135)
