from PIL import Image, ImageDraw, ImageFont
import time
import cv2 as cv
import numpy as np
from Character import Character
from colorsys import hsv_to_rgb
from Joystick import Joystick
from Platform import Platform
from Ledder import Ledder
from Enemy import Enemy_gasi
from Flower import Flower
from StageInfo import Stage1 

def main():
    plat_bottom = Platform((-1000,200,5000))

    x = 0
    stage = Stage1()

    plat_list = [plat_bottom]
    ledder_list = []
    enemy_gasi_list = []
    flower_list = []
    flower_pos_list = stage.flower #꽃 초기위치 
    joystick = Joystick()

    #맵 이미지 설정
    my_map = Image.open('sprite/Map.png')
    
    stage_1 = Image.open(stage.platform_01_img)
    stage_2 = Image.open(stage.platform_o2_img)

    my_map.paste(stage_1,(0,120),stage_1)
    my_map.paste(stage_2,(0,50),stage_2)
    
    cropImage = my_map.crop((0,0,240,240))

    joystick.disp.image(cropImage)  


    #캐릭터 설정 
    character_src = Image.open('sprite/Character.png').convert("RGBA")
    characterImg = character_src.resize((30,33))

    my_character = Character((0,150))
    

    #플랫폼 바닥 설정
    for i in stage.platform_01:
        plat = Platform((i[0],120,i[1]))
        plat_list.append(plat)

    for i in stage.platform_02:
        plat = Platform((i[0],50,i[1]))
        plat_list.append(plat)
    
    #사다리 설정 
    for i in stage.ledder:
        ledder = Ledder((i[0],i[1]))
        ledder_list.append(ledder)

    for ledder in ledder_list:
        ledder_img = Image.open(stage.ledder_img)
        my_map.paste(ledder_img,(ledder.position[0],ledder.position[1]),ledder_img)
    
    #적 - 가시 설정
    for i in stage.enemy_gasi:
        gasi = Enemy_gasi((i[0],i[1]))
        enemy_gasi_list.append(gasi)

    for enemy_gasi in enemy_gasi_list:
        enemy_img = Image.open(stage.enemy_gasi_img)
        my_map.paste(enemy_img,(enemy_gasi.position[0],enemy_gasi.position[1]),enemy_img)

    my_map.save ("sprite/No_Flower.png")
    #꽃 설정 
    for i in stage.flower:
        flower = Flower((i[0],i[1]))
        flower_list.append(flower)

    for flower in flower_list:
        flower_img = Image.open(stage.flower_img)
        my_map.paste(flower_img,(flower.position[0],flower.position[1]),flower_img)

    while True:
        screen_move = 0
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        j = None

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

            x -= 5
            screen_move -= 5

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

            x += 5
            screen_move += 5

        if not joystick.button_A.value: # A pressed
            j = 'a_pressed'
            my_character.ceiling_check(plat_list)

        my_character.move(command)
        my_character.jump(j)
    
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

                


        
        for flower in flower_list:
            flower.collision_check(my_character)

            if (flower.state == 'get'): #꽃을 얻을 경우 리스트에서 제거
                print("Flower Get")
                index = flower_list.index(flower)
                flower_list.pop(index)
                flower_pos_list.pop(index)
                #그림을 새로 그림 (얻은 꽃 제거)
                my_map = Image.open('sprite/No_Flower.png')
                for flower in flower_pos_list:
                    flower_img = Image.open(stage.flower_img)
                    my_map.paste(flower_img,(flower),flower_img)

        
        my_draw = ImageDraw.Draw(cropImage)
                #충돌체크 - 가시 / 바닥 
        my_character.enemy_check(enemy_gasi_list)
        my_character.bottom_check(plat_list)
        
        #캐릭터 현 위치를 보여줌 
        position = tuple(my_character.position)
        cropImage.paste(characterImg, (position[0],position[1]),characterImg)

        joystick.disp.image(cropImage) 
        
        for platform in plat_list:
            my_draw.rectangle(tuple(platform.position),fill = (255,255,255))
        #my_draw.rectangle(tuple(ledder_1.position),fill = (0,0,0))
        #my_draw.rectangle(tuple(enemy_1.position),fill = (0,0,0))
        
        """
        if(flower_1.state != 'get'):
            my_draw.rectangle(tuple(flower_1.position),fill = (50,255,50))
            """
            



if __name__ == '__main__':
    main()