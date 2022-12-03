import numpy as np
import time


class Enemy_gasi:
    def __init__(self, position):
        self.position = np.array([position[0],position[1],position[0]+34,position[1]+18])

class Enemy_monster:
    def __init__(self, spawn_position):
        self.position = np.array([spawn_position[0],spawn_position[1],spawn_position[0] + 48, spawn_position[1] + 38])
        self.move_direction = 0
        self.bottom_check = None
        self.count = 0

    def move(self):
        if (self.bottom_check != None):
            self.position[0] += self.move_direction
            self.position[2] += self.move_direction

        self.count += 1
        if ((self.count % 50) == 0):
            self.move_direction = np.random.randint(-1,2)
            print("Random check", self.move_direction)
            self.count = 0
        
    def bottomCheck(self, bottoms):
        self.bottom_check = None
        for bottom in bottoms:
            collision = self.overlap_bottom(self.position, bottom.position)
        
            if collision:
                self.bottom_check = 'collision'


    def overlap_bottom(self, ego_position, other_position): #ego: 몬스터, otehr: 플랫폼
        return ego_position[0] > other_position[0] - 20 and ego_position[2] < other_position[2] + 20

        
        """
        만약에 바닥 충돌일때만 : 이동
        5초마다 한번씩 방향을 바꿈 (rand -1, 1, 0)
        0이 아니면 state = move
        0이면 None?

        """