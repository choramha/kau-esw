from PIL import Image, ImageDraw, ImageFont
import time
import cv2 as cv
import numpy as np
from Character import Character
from colorsys import hsv_to_rgb
from Joystick import Joystick
from Platform import Platform
from Ledder import Ledder
from Enemy import Enemy
from Flower import Flower
from StageInfo import Stage1 

def main():
    plat_bottom = Platform((-1000,200,5000))

    x = 0
    stage = Stage1()

    plat_list = [plat_bottom]
    ledder_list = []


    joystick = Joystick()

    #맵 이미지 설정
    my_map = Image.open('sprite/Map.png')
    
    stage_1 = Image.open(stage.platform_01_img)
    stage_2 = Image.open(stage.platform_o2_img)

    ledder_1 = Image.open(stage.ledder_img)
    #my_map.paste(ledder_1,(stage.ledder.position))

    my_map.paste(stage_1,(0,120),stage_1)
    my_map.paste(stage_2,(0,50),stage_2)
    my_map.paste(ledder_1,(1095,47),ledder_1)
    
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
    

    ledder_1 = Ledder((1095,47))

    flower_1 = Flower((200,200))

    enemy_1 = Enemy((100,200))

    
    enemy_list = [enemy_1]
    ledder_list = [ledder_1]
    flower_list = [flower_1]

    while True:
        screen_move = 0
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        j = None

        ledder_1.state = None
        
        if (my_character.state != "Enemy Collision"):
            if not joystick.button_U.value:  # up pressed
                ledder_1.collision_check(my_character)

                if ledder_1.state == 'collision':
                    command['up_pressed'] = True
                    command['move'] = True

            if not joystick.button_D.value:  # down pressed
                ledder_1.collision_check(my_character)

                if ledder_1.state == 'collision':
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
    
        cropmap_x1 = 0 + x
        cropmap_x2 = 240 + x

        if cropmap_x1 < 0:
            cropmap_x1 = 0
            cropmap_x2 = 240
        if cropmap_x2 > 1200:
            cropmap_x1 = 1200-240
            cropmap_x2 = 1200

            
        cropImage = my_map.crop((cropmap_x1,0,cropmap_x2,240))
        print(cropmap_x1, cropmap_x2)

        
        if my_character.state == 'move':
            if (cropmap_x1 == 0 or cropmap_x1 == 960):
                screen_move = 0
                print("Check")
            for bottom in plat_list :
                bottom.position[0] = (bottom.position[0] - screen_move)
                bottom.position[2] = (bottom.position[2] - screen_move)
            for enemy in enemy_list:
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
            if (flower.state == 'get'):
                print("Flower Get")
                flower_list.pop(flower_list.index(flower))

        
        my_draw = ImageDraw.Draw(cropImage)
        for platform in plat_list:
            my_draw.rectangle(tuple(platform.position),fill = (255,255,255))
        my_draw.rectangle(tuple(ledder_1.position),fill = (0,0,0))
        my_draw.rectangle(tuple(enemy_1.position),fill = (0,0,0))
        if(flower_1.state != 'get'):
            my_draw.rectangle(tuple(flower_1.position),fill = (50,255,50))

        
        my_character.enemy_check(enemy_list)
        my_character.bottom_check(plat_list)

        position = tuple(my_character.position)
        cropImage.paste(characterImg, (position[0],position[1]),characterImg)

        joystick.disp.image(cropImage) 

if __name__ == '__main__':
    main()