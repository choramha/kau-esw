from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

VELOCITY = 7
MASS = 1.6

class Character:
    def __init__(self, pos): 
        self.appearance = ['sprite/Character/Character_walk1.png','sprite/Character/Character_walk2.png','sprite/Character/Character_walk3.png','sprite/Character/Character_walk4.png',
        'sprite/Character/Character_jump1.png','sprite/Character/Character_jump2.png','sprite/Character/Character_jump3.png','sprite/Character/Character_jump4.png']
        self.state = None
        self.position = np.array([pos[0],pos[1],pos[0]+30,pos[1] + 30], dtype = 'int32')
        self.v = VELOCITY
        self.m = MASS
        self.state_jump = None
        self.bottom = None
        self.health = 3
        self.state_enemy = None
        self.super_time = 0
        self.isjump = 0
        self.direction = None
        self.direction_jump = None
        
    
    def move(self, command = None):
        self.bottom = None
        if command['move'] == False:
            self.state = None
        
        else:
            self.state = 'move'

            if command['up_pressed']:
                self.position[1] -= 10
                self.position[3] -= 10
                self.bottom = "Ledder"

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5
                self.bottom = "Ledder"

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5

            if self.position[0] < 0 :
                self.position[0] = 0
                self.position[2] = 30
            
            if self.position[2] > 240:
                self.position[0] = 210
                self.position[2] = 240
      
    def jump (self, j):
        self.isjump = j

    def jump_update(self):
        if (self.isjump > 0):
            if (self.state_jump == 'Collision'):
                self.v = 0
            self.state_jump = 'jump'
            if self.v > 0:
                F = (0.5 * self.m * (self.v * self.v))
                self.direction_jump = "Jump_UP"
            else:
            # 속도가 0보다 작을때는 아래로 내려감
                F = -(0.5 * self.m * (self.v * self.v))
                self.direction_jump = "Jump_DOWN"

            # 좌표 수정 : 위로 올라가기 위해서는 y 좌표를 줄여준다.
            self.position[1] -= round(F)
            self.position[3] -= round(F)

            # 속도 줄여줌
            self.v -= 1

        else:
            self.v = VELOCITY
            self.direction_jump = None

    def bottom_check(self, bottoms): #바닥 충돌 체크 
        for bottom in bottoms:
            collision = self.overlap_bottom(self.position, bottom.position)

            if collision:
                self.position[3] = bottom.position[1] - 1
                self.position[1] = self.position[3] - 30
                self.bottom = "Collision"

                if self.state_jump == 'jump':
                    self.state_jump = None
                    self.v = 0
                    self.isjump = 0
                break

        if (self.bottom != "Collision" and self.bottom != "Ledder"):
            self.position[1] += 5
            self.position[3] += 5
                

    def ceiling_check(self, ceilings): #천장 충돌 체크 
        if self.state_jump == 'jump':
            for ceiling in ceilings:
                collision = self.overlap_ceiling(self.position, ceiling.position)
                if collision:
                    self.position[1] = ceiling.position[3]
                    self.position[3] = self.position[1] + 30
                    self.state_jump = 'Collision'
                    break

    def enemy_check(self,enemys):
        self.state = None

        if (self.state_enemy == "SUPER"): #적과 부딛히면 일정시간 동안 무적
            self.super_time += 1
            if (self.super_time % 50 == 0):
                self.super_time = 0
                self.state_enemy = None

        for enemy in enemys: 
            collision = self.overlap_enemy(self.position, enemy.position)

            if collision:
                if (self.state_enemy != "SUPER"):
                    self.state_enemy = 'Collision'
                    self.health -= 1

            if(self.state_enemy == 'Collision'):
                if self.position[2] < enemy.position[2]:
                    move = -50
                else :
                    move = 50
                self.position[0] += move 
                self.position[2] += move

                if self.position[0] < 0 :
                    self.position[0] = 0
                    self.position[2] = 30
                
                if self.position[2] > 240:
                    self.position[0] = 210
                    self.position[2] = 240
                self.state_enemy = "SUPER"
                break

    
    
    def overlap_bottom(self, ego_position, other_position): #ego: 캐릭터, otehr: 플랫폼
        return ego_position[0] > other_position[0] - 20 and ego_position[2] < other_position[2] + 20 \
        and ego_position[3] + 3 > other_position[1] and ego_position[3] < other_position[3] + 10

    def overlap_ceiling(self, ego_position, other_position):
        return ego_position[0] > other_position[0] - 15 and ego_position[2] < other_position[2] + 15 \
        and ego_position[1] > other_position[1] - 10 and ego_position[1] < other_position[3] 
    
    def overlap_enemy(self,ego_position,other_position):
        return ego_position[2] > other_position[0] and ego_position[3] > other_position[1] \
        and ego_position[0] < other_position[2] and ego_position[3] < other_position[3] + 5