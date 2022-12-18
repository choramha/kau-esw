from PIL import Image, ImageDraw, ImageFont
import time
import cv2 as cv
import numpy as np
from Character import Character
from colorsys import hsv_to_rgb
from Joystick import Joystick
from Platform import Platform, Goal
from Ledder import Ledder
from Enemy import Enemy_gasi, Enemy_monster
from Flower import Flower
from StageInfo import Stage1,Stage2,Stage3,Stage4,Stage5
import time

plat_list = []
ledder_list = []
enemy_gasi_list = []
flower_list = []
monster_list = []
flower_pos_list = []

#적 물리치거나 아이템 먹을때의 피드백 있음 good 

def main():
    font = ImageFont.truetype("NotoSansMono-Regular.ttf", 18)
    Bold_font = ImageFont.truetype("NotoSansMono-Bold.ttf",24)

    stage_idx = 1
    get_flower = 0
    game_time = 0

    global plat_list
    global ledder_list
    global enemy_gasi_list
    global flower_list
    global monster_list
    global flower_pos_list

    #stage = Stage1()
    my_character = Character((0,150))
    my_map, goal,total_flower = stage_init(stage_idx,my_character)
    character_src = Image.open('sprite/Character.png').convert("RGBA")
    characterImg = character_src.resize((30,33))
    monsterImg = Image.open('sprite/Enemy_monster.png').convert("RGBA")
    monster_src = Image.open('sprite/Monster/Enemy_monster_walk1.png').convert("RGBA")

    startImg = Image.open('sprite/Scene/Start.png')
    
    joystick = Joystick()
    x = 0

    while True:
        joystick.disp.image(startImg)
        if not joystick.button_U.value: 
            break
        if not joystick.button_D.value:
            break
        if not joystick.button_R.value:
            break
        if not joystick.button_L.value:
            break
        if not joystick.button_A.value:
            break
        if not joystick.button_B.value:
            break
        


    while True:
        game_time += 1
        screen_move = 0
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        # j = None

        #사다리 상태 초기화 
        for ledder in ledder_list:
            ledder.state = None

        if not joystick.button_U.value:  # up pressed
        
            for ledder in ledder_list:
                ledder.collision_check(my_character)

                if ledder.state == 'collision': #사다리와 캐릭터가 겹칠때만 Up,Down 가능 
                    command['up_pressed'] = True
                    command['move'] = True

        if not joystick.button_D.value:  # down pressed
            for ledder in ledder_list:
                ledder.collision_check(my_character)

                if ledder.state == 'collision': #사다리와 캐릭터가 겹칠때만 Up,Down 가능 
                    command['down_pressed'] = True
                    command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True
            my_character.direction = "Left"
            x -= 5
            screen_move -= 5

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
            my_character.direction = "Right"
            x += 5
            screen_move += 5

        if not joystick.button_A.value: # A pressed
            if my_character.isjump == 0:
                my_character.jump(1)
                
            
        #캐릭터 충돌 체크 - 바닥, 천장
        my_character.move(command)
        if(my_character.isjump > 0):
            my_character.ceiling_check(plat_list)
        my_character.jump_update()
        my_character.bottom_check(plat_list)
    
        #애니메이션 적용
        if (game_time % 4 == 0):
            character_src = Image.open(my_character.appearance[0]).convert("RGBA")
            monster_src = Image.open('sprite/Monster/Enemy_monster_walk1.png').convert("RGBA")
        elif (game_time % 4 == 1):
            character_src = Image.open(my_character.appearance[1]).convert("RGBA")
            monster_src = Image.open('sprite/Monster/Enemy_monster_walk2.png').convert("RGBA")
        elif (game_time % 4 == 2):
            character_src = Image.open(my_character.appearance[2]).convert("RGBA")
            monster_src = Image.open('sprite/Monster/Enemy_monster_walk3.png').convert("RGBA")
        elif (game_time % 4 == 3) :
            character_src = Image.open(my_character.appearance[3]).convert("RGBA")
            monster_src = Image.open('sprite/Monster/Enemy_monster_walk4.png').convert("RGBA")

        if (my_character.direction_jump == "Jump_UP"):
            character_src = Image.open(my_character.appearance[5]).convert("RGBA")
        elif(my_character.direction_jump == "Jump_DOWN"):
            character_src = Image.open(my_character.appearance[6]).convert("RGBA")

        if (my_character.direction == "Left"):
            character_src = character_src.transpose(Image.FLIP_LEFT_RIGHT)

        #배경 이동
        cropmap_x1 = 0 + x
        cropmap_x2 = 240 + x

        #맵 크기 벗어날 경우 더이상 이동하지 않게 막음 
        if cropmap_x1 < 0:
            cropmap_x1 = 0
            cropmap_x2 = 240
        if cropmap_x2 > 1200:
            cropmap_x1 = 1200-240
            cropmap_x2 = 1200

        cropImage = my_map.crop((cropmap_x1,0,cropmap_x2,240))


        #캐릭터가 이동한 것 처럼 보이게 나머지를 옮김
        if my_character.state == 'move':

            if (cropmap_x1 == 0 or cropmap_x1 == 960):
                screen_move = 0 #맵 끝에 도달한경우 이동 X

            elif (my_character.position[0] > 100 and my_character.position[0] < 150):

                if(command['right_pressed'] == True):
                    my_character.position[0] -= 5
                    my_character.position[2] -= 5

                else: 
                    my_character.position[0] += 5
                    my_character.position[2] += 5

            for bottom in plat_list :
                bottom.position[0] = (bottom.position[0] - screen_move)
                bottom.position[2] = (bottom.position[2] - screen_move)
            for enemy in enemy_gasi_list:
                enemy.position[0] -= screen_move
                enemy.position[2] -= screen_move
            for ledder in ledder_list:
                ledder.position[0] -= screen_move
                ledder.position[2] -= screen_move
            for flower in flower_list:
                flower.position[0] -= screen_move
                flower.position[2] -= screen_move
                
            for monster in monster_list:
                monster.position[0] -= screen_move
                monster.position[2] -= screen_move
                monster.move_range[0] -= screen_move
                monster.move_range[1] -= screen_move
                

            goal.position[0] -= screen_move
            goal.position[2] -= screen_move
                


        
        for flower in flower_list:
            flower.collision_check(my_character)

            if (flower.state == 'get'): #꽃을 얻을 경우 리스트에서 제거
                get_flower += 1
                index = flower_list.index(flower)
                flower_list.pop(index)
                flower_pos_list.pop(index)
                #그림을 새로 그림 (얻은 꽃 제거)
                my_map = Image.open('sprite/No_Flower.png')
                for flower in flower_pos_list:
                    flower_img = Image.open('sprite/Flower.png')
                    my_map.paste(flower_img,(flower),flower_img)

        
        my_draw = ImageDraw.Draw(cropImage)
            #충돌체크  
        for monster in monster_list:
            monster.bottomCheck()
            monster.move()
            if (monster.move_direction <= 0):
                monsterImg = monster_src
            else : 
                monsterImg = monster_src.transpose(Image.FLIP_LEFT_RIGHT)
            cropImage.paste(monsterImg, (monster.position[0],monster.position[1]),monsterImg)
    
        my_character.enemy_check(enemy_gasi_list)
        my_character.enemy_check(monster_list)
        goal.collision_check(my_character)

        #캐릭터 현 위치를 보여줌 
        position = tuple(my_character.position)

        characterImg = character_src.resize((30,33))

        cropImage.paste(characterImg, (position[0],position[1]),characterImg)

        flowerImg = Image.open('sprite/Flower.png').convert("RGBA")
        small_flowerImg = flowerImg.resize((15,15))
        cropImage.paste(small_flowerImg,(5,5),small_flowerImg)
        # 바닥, 가시 실제 위치 시각적으로 보여줌 (#DEBUG)
        """
        my_draw.rectangle(tuple(goal.position),fill = (0,0,0))
        for platform in plat_list:
            my_draw.rectangle(tuple(platform.position),fill = (255,255,255,50))
        for enemy_gasi in enemy_gasi_list:
            my_draw.rectangle(tuple(enemy_gasi.position),fill = (255,255,255,50))
        """
        #골대에 닿을 경우 스테이지 넘어감 
        
        # 체력이 0 이하가 되거나 캐릭터가 낭떨어지에 떨어지면 게임오버 
        if (my_character.health <= 0 or my_character.position[1] > 240 ): 
            game_over_msg1 = "GAME OVER"
            game_over_msg2 = "press B button \n  to Retry"
            my_draw.rectangle((0,0,240,240), fill = (0,0,0))
            my_draw.text((50,80),game_over_msg1,fill = (255,255,255),font = Bold_font)
            my_draw.text((40,120),game_over_msg2,fill=(255,255,255),font = font,spacing = 0)

            if not joystick.button_B.value: #B버튼을 눌러 스테이지 재도전
                x = 0
                get_flower = 0
                my_map,goal,total_flower = stage_init(stage_idx,my_character)

        else : #체력 수 만큼 하트 이미지를 보여줌 
            heartImgSrc = "heart_" + str(my_character.health) + ".png"
            heartImg = Image.open('sprite/heart/'+heartImgSrc)
            heartImg = heartImg.resize((57,15))
            cropImage.paste(heartImg,(180, 5),heartImg)

        if (goal.state == 'clear'):
            if(get_flower == total_flower):
                if (stage_idx == 5): #모든 스테이지 클리어
                    break
            
                else:
                    stage_idx += 1
                    goal.state == None
                    x = 0
                    get_flower = 0
                    my_map,goal,total_flower = stage_init(stage_idx,my_character)
            else:
                msg = "Get All Flower!!"
                my_draw.text((40,80),msg,fill = (0,0,0), font = font)
                goal.state = None
            
        
        text = str(get_flower) + "/" + str(total_flower)
        my_draw.text((25,0),text,fill = (255,255,255),font = font)
    


        #혹시 천장을 뚫고 나갔을 경우를 대비 
        if (my_character.position[3] < 0):
            my_character.position[1] = 0
            my_character.position[3] = 30
        
        joystick.disp.image(cropImage)

    for i in range(1,9):
        clear_src = 'sprite/Scene/Clear' + str(i) + '.png'
        clear = Image.open(clear_src)
        time.sleep(0.5)
        joystick.disp.image(clear)
    while True:
        clear = Image.open('sprite/Scene/Clear9.png')
        joystick.disp.image(clear)


            
def stage_init(stage_idx,my_character):
    global plat_list
    global ledder_list
    global enemy_gasi_list
    global flower_list
    global monster_list
    global flower_pos_list

    if (stage_idx == 1):
        stage = Stage1()
    elif(stage_idx == 2):
        stage = Stage2()
    elif(stage_idx == 3):
        stage = Stage3()
    elif(stage_idx == 4):
        stage = Stage4()
    elif(stage_idx == 5):
        stage = Stage5()
    else:
        print("ERROR!!!!!!")

        #캐릭터 설정 

    character_src = Image.open('sprite/Character.png').convert("RGBA")
    characterImg = character_src.resize((30,33))

    ledderImg = Image.open('sprite/Ledder.png').convert("RGBA")
    flowerImg = Image.open('sprite/Flower.png').convert("RGBA")
    enemy_gasiImg = Image.open('sprite/Enemy_gasi.png').convert("RGBA")
    goalImg = Image.open('sprite/Goal.png').convert("RGBA")
    
    my_character.position[0] = 0
    my_character.position[1] = 150
    my_character.position[2] = 30
    my_character.position[3] = 180

    #리스트 비우기
    plat_ceiling = Platform((-100,-60,5000,49))
    plat_list.clear()
    ledder_list.clear()
    enemy_gasi_list.clear()
    flower_list.clear()
    monster_list.clear()
    flower_pos_list = stage.flower #꽃 초기위치 
    joystick = Joystick()
    my_character.health = 3

    #맵 이미지 설정
    my_map = Image.open('sprite/Map.png')
    
    stage_img = Image.open(stage.platform_img)

    my_map.paste(stage_img,(0,0),stage_img)
    
    cropImage = my_map.crop((0,0,240,240))

    #플랫폼 바닥 설정
    
    for i in stage.platform_01:
        plat = Platform((i[0],200,i[1],500))
        plat_list.append(plat)
    for i in stage.platform_02:
        plat = Platform((i[0],120,i[1],16))
        plat_list.append(plat)
    for i in stage.platform_03:
        plat = Platform((i[0],84,i[1],16))
        plat_list.append(plat)
    for i in stage.platform_04:
        plat = Platform((i[0],50,i[1],16))
        plat_list.append(plat)
    plat_list.append(plat_ceiling)
    
    #사다리 설정 
    for i in stage.ledder:
        ledder = Ledder((i[0],i[1]))
        ledder_list.append(ledder)

    for ledder in ledder_list:
        my_map.paste(ledderImg,(ledder.position[0],ledder.position[1]),ledderImg)
    
    #적 - 가시 설정
    for i in stage.enemy_gasi:
        gasi = Enemy_gasi((i[0],i[1]))
        enemy_gasi_list.append(gasi)

    for enemy_gasi in enemy_gasi_list:
        my_map.paste(enemy_gasiImg,(enemy_gasi.position[0],enemy_gasi.position[1]),enemy_gasiImg)

    goal = Goal((stage.goal[0],stage.goal[1]))  
    my_map.paste(goalImg,(goal.position[0],goal.position[1]),goalImg)

    my_map.save ("sprite/No_Flower.png")
    #꽃 설정 
    for i in stage.flower:
        flower = Flower((i[0],i[1]))
        flower_list.append(flower)

    for flower in flower_list:
        my_map.paste(flowerImg,(flower.position[0],flower.position[1]),flowerImg)

    #적 - 몬스터 설정 
    for i in stage.enemy_monster:
        monster = Enemy_monster((i[0],i[1]),(i[2],i[3]))
        monster_list.append(monster)

    return my_map, goal, len(flower_list)


if __name__ == '__main__':
    main()