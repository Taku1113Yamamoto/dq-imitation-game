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

        


class Battle:
    def __init__(self,player,monster):
        self.player = player
        self.monster = monster

        #変数のboolの値でキー入力を制御して攻撃アクションを作っていく

        self.battle_now = False  #バトル画面を表示する
        self.battle_anim_count = 0  #時間で画面遷移させるのに用いる

        self.command_selecting = False  #攻撃アクションの選択の表示
        self.command_select_tri = False  #攻撃アクションの選択ボタンの表示
        self.command_arrow_num = 0  #攻撃アクションの選択ボタンの数字
        self.command_arrow_max_num = 4 

        self.magic_selecting = False  #呪文の選択の表示
        self.magic_attack = False  #呪文攻撃かどうかを判別、攻撃時の文字を変更する
        self.magic_select_tri = False  
        self.magic_arrow_num = 0
        self.magic_arrow_max_num = 0

        self.monster_selecting = False  #攻撃するモンスターの選択を可能に

        #コメントの表示と画面遷移に用いる
        self.attack_player_anim = False
        self.magic_player_anim = False
        self.guard_anim = False
        self.item_selecting = False
        self.attack_monster_anim = False
        self.defeated_monster = False
        self.you_defeate = False
        self.you_lose = False
        self.lv_up_anim = False
        self.lv_up_anim_2 = False

        self.item_select_tri = False
        self.item_select_num = 0
        self.use_item = []
        self.use_item_anim = False



        self.damage = 0 
        
       
        self.escape_success = 0 #この値でにげるが成功するかどうかを決める

        self.random_walk = random.randrange(5, 10) #エンカウントまでの歩数

        

 
    






    def update(self):
        if(self.player.move_count == self.random_walk):
            self.battle_now = True
            

    def battleAnim(self,screen):
        self.battle_anim_count += 1
        self.screen = screen
        if(self.battle_anim_count < 20):
            

            if((self.battle_anim_count/5)%2):
                self.screen.fill(BLACK)
            else:
                self.screen.fill(WHITE)
        else:
            self.screen.fill(BLACK)
            self.drawMonster()
        
        if(self.battle_anim_count > 40 and self.battle_anim_count < 80):
            self.drawText(str(self.monster.name)+"が　あらわれた。","","","")

        if(self.battle_anim_count > 80):
            self.drawStatas()

        if(self.battle_anim_count == 80):
            self.command_selecting = True
            self.command_select_tri = True
            self.magic_select_tri = True
            

        if(self.command_selecting):
            self.drawComand()
            self.drawMonsterList()

            if(self.command_select_tri):
                if(self.command_arrow_num>3):
                    self.command_arrow_num_correct = 3
                else:
                    self.command_arrow_num_correct = self.command_arrow_num
                self.drawTri(65,307+self.command_arrow_num_correct*37)

        if(self.magic_selecting):
            self.drawMagicList() 
            if(self.magic_select_tri):
                self.magic_arrow_max_num = len(self.player.magic_list)-1
                if(self.magic_arrow_num >3):
                    self.magic_arrow_num_correct = 3
                else:
                    self.magic_arrow_num_correct = self.magic_arrow_num
                self.drawTri(205,307+self.magic_arrow_num_correct*37)
                self.player.selected_magic = self.player.magic_list[self.magic_arrow_num][1]
                self.player.selected_magic_mp = int(self.player.magic_list[self.magic_arrow_num][2])
                self.player.selected_magic_damage = int(self.player.magic_list[self.magic_arrow_num][3])
                self.player.selected_magic_heal = int(self.player.magic_list[self.magic_arrow_num][4])

        if(self.monster_selecting):
            self.drawTri(235,307)

        if self.item_selecting:
            pygame.draw.rect(self.screen,BLACK,Rect(210,245,180,215))
            pygame.draw.rect(self.screen,WHITE,Rect(210,245,180,215),5)
            for i in range (len(self.player.item_list)):
                drawChar(self.screen,moji.han_to_zen(self.player.item_list[i][1]),240,243+i*40)
        
        if self.item_select_tri:
            self.drawTri(220,262+self.item_select_num*40)

        if self.use_item_anim:
            drawText(self.screen,"ゆうしゃは　"+moji.han_to_zen(str(self.use_item[1]))+"を　つかった！","ゆうしゃの　キズが　かいふくした！","","")

        

        if(self.guard_anim):
            self.drawText("ゆうしゃは　みをまもっている。","","","")


        if(self.escape_success == 1):
            self.drawText("ゆうしゃは　にげだした！","","","")

        if(self.escape_success == 2):
            self.drawText("ゆうしゃは　にげだした！","しかし　まわりこまれてしまった！","","")



        if(self.attack_player_anim):
            self.drawText("ゆうしゃの　こうげき！",str(self.damage)+"の　ダメージ！","","")

        if(self.magic_player_anim):
            if self.player.selected_magic_heal == 0:
                self.drawText("ゆうしゃは　"+self.player.magic_list[self.player.selected_magic][1]+"を　となえた！",str(self.monster.name)+"に　"+str(self.player.selected_magic_damage)+"の　ダメージ！","","")
            else:
                self.drawText("ゆうしゃは　"+self.player.magic_list[self.player.selected_magic][1]+"を　となえた！","ゆうしゃの　きずが　かいふくした！","","")



        if(self.attack_monster_anim):
            self.drawText(str(self.monster.name)+"の　こうげき！","ゆうしゃに　"+str(self.damage)+"の　ダメージ！","","")

        if(self.you_defeate):
            self.drawText(str(self.monster.name)+"を　やっつけた。",str(self.monster.exp)+"ポイントの　けいけんちを　かくとく。",str(self.monster.gold)+"ゴールドを　てにいれた。","")

        if(self.lv_up_anim):
            self.drawText("ゆうしゃは　レベルが　あがった！","ちからが　"+str(self.player.lv_tables[self.player.lv][3]-self.player.lv_tables[self.player.lv-1][3])+"ポイント　あがった！","みのまもりが　"+str(self.player.lv_tables[self.player.lv][4]-self.player.lv_tables[self.player.lv-1][4])+"ポイント　あがった！","さいだいHPが　"+str(self.player.lv_tables[self.player.lv][1]-self.player.lv_tables[self.player.lv-1][1])+"ポイント　あがった！")
        
        if(self.lv_up_anim_2):
            self.drawText("さいだいMPが　"+str(self.player.lv_tables[self.player.lv][2]-self.player.lv_tables[self.player.lv-1][2])+"ポイント　あがった！","","","")
            
        
        if(self.you_lose):
            self.drawText("ゆうしゃは　しんでしまった！","しょじきんが　はんぶんになった。","","")
                    

        
    def drawTri(self,x,y):
        if(self.battle_anim_count%80 >30):
            pygame.draw.polygon(self.screen,WHITE,[(x,y+20),(x+13,y+10),(x,y)])
        else:
            pygame.draw.polygon(self.screen,BLACK,[(x,y+20),(x+13,y+10),(x,y)])



    def drawChar(self,char,x,y):
        self.text_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.text = self.text_font.render(char,False,WHITE)
        self.screen.blit(self.text,(x,y))


    def drawStatas(self):
        pygame.draw.rect(self.screen,WHITE,Rect(50,20,160,120),5)
        pygame.draw.rect(self.screen,BLACK,Rect(90,15,80,10))
        self.drawChar("ゆうしゃ",92,-8)
        self.drawChar("Ｈ　" + moji.han_to_zen(str(self.player.hp)),92,23)
        self.drawChar("Ｍ　" + moji.han_to_zen(str(self.player.mp)),92,55)
        if(self.player.lv <10):
            self.drawChar("ゆ：　" + moji.han_to_zen(str(self.player.lv)),92,87)
        else:
            self.drawChar("ゆ：" + moji.han_to_zen(str(self.player.lv)),92,87)



    def drawText(self,text1,text2,text3,text4):
        pygame.draw.rect(self.screen,WHITE,Rect(70,280,500,180),5)
        self.drawChar(moji.han_to_zen(text1),90,290)
        self.drawChar(moji.han_to_zen(text2),90,323)
        self.drawChar(moji.han_to_zen(text3),90,356)
        self.drawChar(moji.han_to_zen(text4),90,389)

    def drawMonster(self):
        image = pygame.image.load(self.monster.image)
        self.screen.blit(image,(260,140))
    
    def drawComand(self):
        pygame.draw.rect(self.screen,WHITE,Rect(50,280,160,180),5)
        pygame.draw.rect(self.screen,BLACK,Rect(90,275,80,10))
        self.drawChar("ゆうしゃ",92,252)
        commands = [ "こうげき","じゅもん","ぼうぎょ","にげる","どうぐ"]
        for i in range (4):
            if(self.command_arrow_num<4):
                self.drawChar(commands[i],92,288+37*i)
            else:
                self.drawChar(commands[self.command_arrow_num-3+i],92,288+37*i)
    
    def drawMonsterList(self):
        pygame.draw.rect(self.screen,WHITE,Rect(220,280,400,100),5)
        self.drawChar(self.monster.name,262,288)
        self.drawChar("ー　１ひき",480,288)

    def drawMagicList(self):
        # self.magic_arrow = num
        pygame.draw.rect(self.screen,BLACK,Rect(190,280,160,180))
        pygame.draw.rect(self.screen,WHITE,Rect(190,280,160,180),5)
        magic_count = len(self.player.magic_list)
        if magic_count<4:
            for i in range (magic_count):
                self.drawChar(self.player.magic_list[i][1],232,288+37*i)
        else:
            for i in range (4):
                if(self.magic_arrow_num<4):
                    self.drawChar(self.player.magic_list[i][1],232,288+37*i)
                else:
                    self.drawChar(self.player.magic_list[self.magic_arrow_num-3+i][1],232,288+37*i)
    
