from PIL import Image, ImageDraw, ImageFont
import numpy as np

VELOCITY = 8
MASS = 1

class Character:
    def __init__(self, pos): 
        self.apperance = 'sprite/Character.png'
        self.state = None
        self.position = np.array([pos[0],pos[1],pos[0]+30,pos[1] + 30], dtype = 'int32')
        self.v = VELOCITY
        self.m = MASS
        self.state_jump = None
        self.bottom = None
        self.health = 3
        
    
    def move(self, command = None):
        if command['move'] == False:
            self.state = None
        
        else:
            if self.state != 'Enemy Collision':
                self.state = 'move'

                if command['up_pressed']:
                    self.position[1] -= 5
                    self.position[3] -= 5

                if command['down_pressed']:
                    self.position[1] += 5
                    self.position[3] += 5

                if command['left_pressed']:
                    self.position[0] -= 5
                    self.position[2] -= 5
                    
                if command['right_pressed']:
                    self.position[0] += 3
                    self.position[2] += 3

                if self.position[0] < 0 :
                    self.position[0] = 0
                    self.position[2] = 40
                
                if self.position[2] > 240:
                    self.position[0] = 200
                    self.position[2] = 240
                

                
                
      
    
    def jump(self, j = None):
        self.state_jump = None
        if j == 'a_pressed':
            if (self.state_jump == 'Collision'):
                self.v = 0
                print("Jump - Collision")
            self.state_jump = 'jump'
            if self.v > 0:
                F = (0.5 * self.m * (self.v * self.v))
            else:
            # 속도가 0보다 작을때는 아래로 내려감
                F = -(0.5 * self.m * (self.v * self.v))
                if self.v < ( 0 - VELOCITY): #점프 시작 위치보다 밑으로 내려가는걸 방지 
                    self.v = 0

            # 좌표 수정 : 위로 올라가기 위해서는 y 좌표를 줄여준다.
            self.position[1] -= round(F)
            self.position[3] -= round(F)

            # 속도 줄여줌
            self.v -= 1.5

            #충돌 범위 벗어나면 y값 이전, 이후 비교해서 사이에 바닥 있는지 체크하기! 



        else:
            self.v = VELOCITY

    def bottom_check(self, bottoms):
        for bottom in bottoms:
            collision = self.overlap_bottom(self.position, bottom.position)

            if collision:
                self.position[3] = bottom.position[1] - 1
                self.position[1] = self.position[3] - 30
                

                if self.state_jump == 'jump':
                    self.state_jump = None
                    self.v = 0

    def ceiling_check(self, ceilings):
        if self.state_jump == 'jump':
            for ceiling in ceilings:
                collision = self.overlap_ceiling(self.position, ceiling.position)
                if collision:
                    self.position[1] = ceiling.position[3]
                    self.position[3] = self.position[1] + 30
                    self.state_jump == 'Collision'

    def enemy_check(self,enemys):
        self.state = None
        for enemy in enemys: 
            collision = self.overlap_enemy(self.position, enemy.position)

            if collision:
                self.health -= 1
                self.state = 'Enemy Collision'
                print(self.health)
            
            if(self.state == 'Enemy Collision'):
                if self.position[2] < enemy.position[2]:
                    move = -30
                else :
                    move = 30

                self.position[0] += move 
                self.position[2] += move

                if self.position[0] < 0 :
                    self.position[0] = 0
                    self.position[2] = 40
                
                if self.position[2] > 240:
                    self.position[0] = 200
                    self.position[2] = 240

    
    
    def overlap_bottom(self, ego_position, other_position): #ego: 캐릭터, otehr: 플랫폼
        return ego_position[0] > other_position[0] - 20 and ego_position[2] < other_position[2] + 20 \
        and ego_position[3] + 3 > other_position[1] and ego_position[3] < other_position[3] 

    def overlap_ceiling(self, ego_position, other_position):
        return ego_position[0] > other_position[0] - 10 and ego_position[2] < other_position[2] + 10 \
        and ego_position[1] > other_position[1] - 20 and ego_position[1] < other_position[3] 
    
    def overlap_enemy(self,ego_position,other_position):
        return ego_position[2] > other_position[0] and ego_position[3] > other_position[1] \
        and ego_position[0] < other_position[2] and ego_position[3] < other_position[3] + 5