import pygame
import sys
import random
from pygame.locals import *

import mojimoji as moji

import title as tl
import menu as mn
import item as it
import player as pl
import map_map as mp
import town as tw
import shop as sp
import inn as nn
import monster as ms
import battle as bt

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

         
                

                               


def main():
    pygame.init()

    # メイン画面の初期化,rectでサイズを指定
    screen  = pygame.display.set_mode(SCREEN_RECT.size)
    
    # メイン画面のタイトル
    pygame.display.set_caption("exit: press esc")

    clock = pygame.time.Clock()

    title = tl.Title(screen)

    item = it.Item()
    
    menu_display = False

    #主人公の画像読み込み
    player = pl.Player("assets/pipo-charachip029c.png",title,item)
    group = pygame.sprite.RenderUpdates()
    group.add(player)

    field_map = mp.Map(screen,"assets/maps/field-map.txt",player)

    player.mapSet(field_map)

    town_map = mp.Map(screen,"assets/maps/town-map.txt",player)
    town = tw.Town(player,field_map,5)

    cave_map = mp.Map(screen,"assets/maps/cave-map.txt",player)
    cave = tw.Town(player,field_map,4)

    monster = ms.Monster()
    battle = bt.Battle(player,monster)

    menu = mn.Menu(screen,player)

    shop = sp.Shop(menu,player,screen,item)
    inn = nn.Inn(menu,player,screen,item)

    global_count = 0

    def dataSave():
        player.saved_player_data += (str(player.hp) + "," + str(player.mp) + "," + str(player.exp) + "," + str(player.gold) + "," + str(player.wx) + "," +  str(player.wy)+ ",")
        if field_map.map_display:
            player.saved_player_data += "0" 
        elif town.map_display:
            player.saved_player_data += "1" 
        elif cave.map_display:
            player.saved_player_data += "2"  
        for i in range (len(player.item_list)):
            player.saved_player_data += ("," + str(player.item_list[i][0]))
        if len(player.item_list)<5:
            for i in range(5-len(player.item_list)):
                player.saved_player_data += "," + str(0)
        with open ("assets/saved-player-data.txt",mode = "w") as fi:
            fi.write(player.saved_player_data)
    
    if player.where == 0:
        field_map.map_display = True
        town.map_display = False
        cave.map_display = False
    elif player.where == 1:
        field_map.map_display = False
        town.map_display = True
        cave.map_display = False
    if player.where == 2:
        field_map.map_display = False
        town.map_display = False
        cave.map_display = True

    while(True):
        menu_display = menu.menu_display

        pygame.event.clear()

        global_count += 1

        if title.title_display:
            title.update()
            title.drawTri(240,317+50*title.title_select_num,global_count)
        
        elif shop.shop_display:
            shop.shopAnim()

        elif inn.inn_display:
            inn.innAnim()
        
        else:
            if not town.map_display:
                battle.update()

            if(not battle.battle_now):
                
                if(field_map.map_display): 
                    player.mapSet(field_map)
                    field_map.draw(0)
                    if player.wx <= 15 and player.wy <= 11:
                        monster.decideMonster("assets/monster-list/field-monsters.txt")
                    elif player.wx <= 15 and player.wy > 11:
                        monster.decideMonster("assets/monster-list/field-monsters2.txt")
                    elif player.wx > 15 and player.wy <= 11:
                        monster.decideMonster("assets/monster-list/field-monsters3.txt")
                    elif player.wx > 15 and player.wy > 11:
                        monster.decideMonster("assets/monster-list/field-monsters4.txt")
                    town.visited(8,5)
                    cave.visited(18,28)
                

                elif(town.map_display):
                    player.mapSet(town_map)
                    town_map.draw(1)
                    shop.update(3,2)
                    inn.update(6,2)
                    town.exit(6)


                elif(cave.map_display):
                    player.mapSet(cave_map)
                    monster.decideMonster("assets/monster-list/cave-monsters.txt")
                    cave_map.draw(8)
                    cave.exit(29)
                
                group.update(menu_display)
                group.draw(screen)

            else:

                battle.battleAnim(screen)

        if menu.menu_display and not title.title_display:
            
            menu.update()
            # menu.drawTri(60,39+menu.menu_select_num*40,global_count)
        
        # フレームレートの設定
        clock.tick(60)
    

        #イベント
        #keyはまとめてここに書かないと思った挙動にならない、正直めんどくさすぎる
        for event in pygame.event.get():

            # 終了イベント
            if event.type == QUIT:
                dataSave()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    dataSave()
                    pygame.quit()
                    sys.exit()

                if not battle.battle_now:
                    if not menu.menu_display:
                        if event.key == pygame.K_RETURN:
                            menu.menu_display = True
                    else:
                        if event.key == pygame.K_RETURN:
                            menu.menu_display = False
                            menu.show_statas = False
                            menu.show_items = False
                            menu.show_magics = False
                            menu.item_select_tri = False
                            menu.use_item_anim = False
                
                shop.KeyEvent(event)
                # if shop.shop_display:
                #     player.moving_wait = False

                    
                #     if event.key==pygame.K_DOWN:
                #         if(shop.shop_select_num == 2):
                #             shop.shop_select_num = 0
                #         else:
                #             shop.shop_select_num += 1
                        
                #     if event.key==pygame.K_UP:
                #         if(shop.shop_select_num == 0):
                #             shop.shop_select_num = 2
                #         else:
                #             shop.shop_select_num -= 1

                    
                    # if event.key==pygame.K_RIGHT :
                    #     if len(player.item_list) < 5:
                    #         if shop.shop_select_num == 0 and player.gold >= int(item.all_item_list[0][3]):
                    #             player.item_list.append(item.all_item_list[0])
                    #             player.gold -= int(item.all_item_list[0][3])
                    #         elif shop.shop_select_num == 1 and player.gold >= int(item.all_item_list[1][3]):
                    #             player.item_list.append(item.all_item_list[1])
                    #             player.gold -= int(item.all_item_list[1][3])
                    #     if shop.shop_select_num == 2:
                    #         shop.shop_display = False
                    #         player.wy += 1

                if inn.inn_display:
                    player.moving_wait = False
                    
                    if event.key==pygame.K_DOWN:
                        if(inn.inn_select_num == 1):
                            inn.inn_select_num = 0
                        else:
                            inn.inn_select_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(inn.inn_select_num == 0):
                            inn.inn_select_num = 1
                        else:
                            inn.inn_select_num -= 1
                    
                    if event.key==pygame.K_RIGHT:
                        if inn.inn_select_num == 0 and player.gold >= 10:
                            player.gold -= 10
                            player.hp,player.mp = player.max_hp,player.max_mp
                        elif inn.inn_select_num == 1:
                            inn.inn_display = False
                            player.wy += 1


                
                if menu.menu_display:
                    if event.key==pygame.K_DOWN:
                        if(menu.menu_select_num == 2):
                            menu.menu_select_num = 0
                        else:
                            menu.menu_select_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(menu.menu_select_num == 0):
                            menu.menu_select_num = 2
                        else:
                            menu.menu_select_num -= 1

                    if event.key==pygame.K_LEFT:
                        menu.show_statas = False
                        menu.show_items = False
                        menu.show_magics = False
                        menu.item_select_tri = False
                        menu.magic_select_tri = False

                       

                    if event.key==pygame.K_RIGHT and not menu.item_select_tri and not menu.magic_select_tri:
                        if menu.menu_select_num == 0:
                            menu.show_statas = True
                        elif menu.menu_select_num == 1:
                            menu.show_items = True
                            menu.item_select_tri = True
                            wait_count_item_show  = global_count
                        elif menu.menu_select_num == 2:
                            menu.show_magics = True
                            menu.magic_select_tri = True
                            wait_count_magic_show  = global_count

                if menu.item_select_tri == True and wait_count_item_show+3 < global_count:
                    if event.key==pygame.K_DOWN:
                        if(menu.item_select_num == len(player.item_list)-1):
                            menu.item_select_num = 0
                        else:
                            menu.item_select_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(menu.item_select_num == 0):
                            menu.item_select_num = len(player.item_list)-1
                        else:
                            menu.item_select_num -= 1
                    if event.key==pygame.K_RIGHT:
                        menu.show_items = False
                        menu.item_select_tri = False
                        menu.use_item_anim = True
                        wait_count_item_anim = global_count 
                        menu.use_item = player.item_list.pop(menu.item_select_num)
                        player.hp += int(menu.use_item[2])
                        if player.hp > player.max_hp:
                            player.hp = player.max_hp
                        
                
                if menu.use_item_anim == True and wait_count_item_anim+3 < global_count:
                    menu.use_item_anim = False

                if menu.magic_select_tri == True and wait_count_magic_show+3 < global_count:
                    if event.key==pygame.K_DOWN:
                        if menu.magic_arrow_num == menu.magic_arrow_max_num:
                            menu.magic_arrow_num = 0
                        else:
                            menu.magic_arrow_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(menu.magic_arrow_num == 0):
                            menu.magic_arrow_num = menu.magic_arrow_max_num
                        else:
                            menu.magic_arrow_num -= 1
                    if event.key==pygame.K_RIGHT  and player.mp > player.selected_magic_mp and player.selected_magic_heal == 1:
                        menu.show_magics = False
                        menu.magic_select_tri = False
                        menu.use_magic_anim = True
                        player.mp -= player.selected_magic_mp
                        player.hp += player.selected_magic_damage
                        if player.hp > player.max_hp:
                            player.hp = player.max_hp
                        wait_count_magic_anim = global_count 
                        
                
                if menu.use_magic_anim == True and wait_count_magic_anim+3 < global_count:
                    menu.use_magic_anim = False

                

                   
                if title.title_display:
                    if event.key==pygame.K_DOWN:
                        if(title.title_select_num == 1):
                            title.title_select_num = 0
                        else:
                            title.title_select_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(title.title_select_num == 0):
                            title.title_select_num = 1
                        else:
                            title.title_select_num -= 1

                    if event.key==pygame.K_RIGHT:
                        title.title_display = False
                        player.moving_wait = False
                        player.parameterSet()
                        if player.where == 0:
                            field_map.map_display = True
                            town.map_display = False
                            cave.map_display = False
                        elif player.where == 1:
                            field_map.map_display = False
                            town.map_display = True
                            cave.map_display = False
                        elif player.where == 2:
                            field_map.map_display = False
                            town.map_display = False
                            cave.map_display = True
                        player.itemSet(item)
                        for i in range (len(player.magic_list_num)):
                            player.magic_list.append(player.all_magic_list[player.magic_list_num[i]-1])


                if battle.command_select_tri:
                    if event.key==pygame.K_DOWN:
                        if(battle.command_arrow_num == battle.command_arrow_max_num):
                            battle.command_arrow_num = 0
                        else:
                            battle.command_arrow_num += 1
                        
                    if event.key==pygame.K_UP:
                        if(battle.command_arrow_num == 0):
                            battle.command_arrow_num = battle.command_arrow_max_num
                        else:
                            battle.command_arrow_num -= 1
                    
                    if event.key == pygame.K_RIGHT:
                        battle.command_select_tri =False
                        if(battle.command_arrow_num == 0):
                            battle.monster_selecting = True
                            wait_count_select_monster = battle.battle_anim_count
                        elif(battle.command_arrow_num == 1):
                            battle.magic_selecting = True
                            battle.magic_attack = True
                            wait_count_select_magic = battle.battle_anim_count
                        elif(battle.command_arrow_num == 2):
                            battle.guard_anim = True
                            battle.command_selecting = False
                            wait_count_guard_anim = battle.battle_anim_count
                        elif battle.command_arrow_num == 3:
                            wait_count_escape_anim = battle.battle_anim_count
                            battle.command_selecting = False
                            battle.random_walk = 5 + battle.battle_anim_count%10
                            if(global_count%100 + player.lv*3) >= 100:
                                battle.escape_success = 1
                            else:
                                battle.escape_success = 2
                        elif battle.command_arrow_num == 4:
                            battle.item_select_tri = True
                            battle.item_selecting = True
                            wait_count_item_show_battle  = battle.battle_anim_count

                if battle.item_select_tri:
                    if wait_count_item_show_battle+3 < battle.battle_anim_count:
                        if event.key==pygame.K_DOWN:
                            if(battle.item_select_num == len(player.item_list)-1):
                                battle.item_select_num = 0
                            else:
                                battle.item_select_num += 1
                            
                        if event.key==pygame.K_UP:
                            if(battle.item_select_num == 0):
                                battle.item_select_num = len(player.item_list)-1
                            else:
                                battle.item_select_num -= 1
                        if event.key==pygame.K_RIGHT:
                            battle.item_selecting = False
                            battle.item_select_tri = False
                            battle.command_selecting = False
                            battle.use_item_anim = True
                            wait_count_item_anim = global_count 
                            battle.use_item = player.item_list.pop(battle.item_select_num)
                            player.hp += int(battle.use_item[2])
                            if player.hp > player.max_hp:
                                player.hp = player.max_hp
                
                if battle.use_item_anim == True and wait_count_item_anim+3 < global_count:
                    battle.use_item_anim = False
                    battle.attack_monster_anim = True
                    wait_count_restart = battle.battle_anim_count

                if battle.magic_selecting:
                    
                    if event.key==pygame.K_DOWN and (wait_count_select_magic+3) < battle.battle_anim_count:
                        if(battle.magic_arrow_num == battle.magic_arrow_max_num):
                            battle.magic_arrow_num = 0
                        else:
                            battle.magic_arrow_num += 1
                        
                    if event.key==pygame.K_UP and (wait_count_select_magic+3) < battle.battle_anim_count:
                        if(battle.magic_arrow_num == 0):
                            battle.magic_arrow_num = battle.magic_arrow_max_num
                        else:
                            battle.magic_arrow_num -= 1

                    if event.key == pygame.K_RIGHT  and (wait_count_select_magic+3) < battle.battle_anim_count and player.mp > player.selected_magic_mp:
                        battle.monster_selecting = True
                        battle.magic_selecting = False
                        wait_count_select_monster = battle.battle_anim_count
                        player.selected_magic = battle.magic_arrow_num

                    if event.key == pygame.K_LEFT  and (wait_count_select_magic+3) < battle.battle_anim_count:
                        battle.magic_selecting = False
                        battle.magic_attack = False
                        battle.command_select_tri =True

                if(battle.monster_selecting):
                    if not battle.magic_attack:
                        if event.key == pygame.K_RIGHT and (wait_count_select_monster+3) < battle.battle_anim_count:
                            battle.monster_selecting = False
                            battle.command_selecting = False
                            battle.attack_player_anim = True
                            wait_count_attack_monster = battle.battle_anim_count
                            if(monster.defence >= player.attack):
                                battle.damage = 1
                            else:
                                battle.damage = player.attack - monster.defence
                        if event.key == pygame.K_LEFT and (wait_count_select_monster+3) < battle.battle_anim_count:
                            battle.monster_selecting = False
                            battle.command_select_tri =True
                    else:
                        if event.key == pygame.K_RIGHT and (wait_count_select_monster+3) < battle.battle_anim_count:
                            battle.monster_selecting = False
                            battle.command_selecting = False                  
                            battle.magic_player_anim = True
                            wait_count_attack_monster = battle.battle_anim_count

                        if event.key == pygame.K_LEFT and (wait_count_select_monster+3) < battle.battle_anim_count:
                            battle.monster_selecting = False
                            battle.magic_selecting =True
                            wait_count_select_magic = battle.battle_anim_count
                
                if(battle.escape_success == 2):
                    if event.key == pygame.K_RIGHT and (wait_count_escape_anim+3) < battle.battle_anim_count:
                        battle.attack_monster_anim = True
                        battle.escape_success = 0
                        wait_count_restart = battle.battle_anim_count
                        if(player.defence >= monster.attack):
                            battle.damage = 1
                        else:
                            battle.damage = monster.attack - player.defence

                if(battle.escape_success == 1):
                    if event.key == pygame.K_RIGHT and (wait_count_escape_anim+3) < battle.battle_anim_count:
                        battle.escape_success = 0
                        battle.battle_now = False
                        battle.battle_anim_count = 0
                        player.move_count = 0
                        battle.random_walk = 5 + battle.battle_anim_count%10
                        monster.random_monster_num = global_count % 100
                        
                        

                
                if(battle.attack_player_anim):
                    if event.key == pygame.K_RIGHT and (wait_count_attack_monster+3) < battle.battle_anim_count:
                        battle.attack_player_anim = False
                        wait_count_restart = battle.battle_anim_count
                        monster.hp -= battle.damage
                        battle.random_walk = 5 + battle.battle_anim_count%6
                        monster.random_monster_num = global_count % 100
                        if(monster.hp <= 0):
                            battle.you_defeate = True
                        else:
                            battle.attack_monster_anim = True
                            if(player.defence >= monster.attack):
                                battle.damage = 1
                            else:
                                battle.damage = monster.attack - player.defence

                if(battle.magic_player_anim):
                    battle.magic_select_tri =False
                    battle.magic_attack = False
                    if event.key == pygame.K_RIGHT and (wait_count_attack_monster+3) < battle.battle_anim_count:
                        battle.magic_player_anim = False
                        wait_count_restart = battle.battle_anim_count
                        if player.selected_magic_heal == 1:
                            player.hp += player.selected_magic_damage
                            if player.hp > player.max_hp:
                                player.hp = player.max_hp
                        else:
                            monster.hp -= player.selected_magic_damage
                        player.mp -= player.selected_magic_mp
                        battle.random_walk = 5 + battle.battle_anim_count%6
                        monster.random_monster_num = global_count % 100
                        if(monster.hp <= 0):
                            battle.you_defeate = True
                        else:
                            battle.attack_monster_anim = True
                            if(player.defence >= monster.attack):
                                battle.damage = 1
                            else:
                                battle.damage = monster.attack - player.defence
                
                if(battle.guard_anim):
                    if event.key == pygame.K_RIGHT and (wait_count_guard_anim+3) < battle.battle_anim_count:
                        battle.guard_anim = False
                        battle.attack_monster_anim = True
                        wait_count_restart = battle.battle_anim_count
                        if(player.defence*2 >= monster.attack):
                            battle.damage = 1
                        else:
                            battle.damage = monster.attack - player.defence*2
                        
                 
                if(battle.attack_monster_anim):
                    if event.key == pygame.K_RIGHT and (wait_count_restart+3) < battle.battle_anim_count:
                        if player.hp > battle.damage:
                            player.hp -= battle.damage
                            battle.battle_anim_count =79
                            battle.attack_monster_anim = False
                        else:
                            battle.random_walk = 5 + battle.battle_anim_count%10
                            monster.random_monster_num = global_count % 100           
                            battle.attack_monster_anim = False
                            battle.you_lose = True
                            wait_count_you_lose = battle.battle_anim_count

                
                if(battle.you_defeate and (wait_count_restart+3) < battle.battle_anim_count):
                    player.exp += monster.exp
                    player.gold += monster.gold
                    if  player.lv == len(player.lv_tables):
                        battle.you_defeate = False
                        battle.battle_now = False
                        player.moving_wait = False
                        battle.battle_anim_count = 0
                        player.move_count = 0
                    elif player.lv_tables[player.lv][5] <= player.exp:
                        battle.you_defeate = False
                        battle.lv_up_anim = True
                        player.parameterSet()
                        wait_count_lv_anim = battle.battle_anim_count
                    else:
                        battle.you_defeate = False
                        battle.battle_now = False
                        player.moving_wait = False
                        battle.battle_anim_count = 0
                        player.move_count = 0
                
                if(battle.lv_up_anim and (wait_count_lv_anim+3) < battle.battle_anim_count):
                    battle.lv_up_anim = False
                    battle.lv_up_anim_2 = True
                    wait_count_lv_anim_2 = battle.battle_anim_count
                
                if battle.lv_up_anim_2 and (wait_count_lv_anim_2+3) < battle.battle_anim_count:
                    battle.lv_up_anim_2 = False
                    battle.battle_now = False
                    player.moving_wait = False
                    battle.battle_anim_count = 0
                    player.move_count = 0

                if(battle.you_lose and (wait_count_you_lose+3) < battle.battle_anim_count):
                    
                    battle.you_lose = False
                    battle.battle_now = False
                    field_map.map_display = True
                    town.map_display = False
                    cave.map_display = False
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                    player.gold = player.gold//2
                    battle.battle_anim_count = 0
                    player.move_count = 0
                    player.wx, player.wy =4, 3
            

  
            if event.type == pygame.KEYUP:
                if not player.moving_wait:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        player.moving_wait = True
            

                        

        # print(player.lv_tables[player.lv][5])

        
        # メイン画面の更新
        pygame.display.update()


                    
 
if __name__ == '__main__':
    main()