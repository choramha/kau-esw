import numpy as np
import time


class Enemy_gasi:
    def __init__(self, position):
        self.position = np.array([position[0],position[1],position[0]+25,position[1]+15])

class Enemy_monster:
    def __init__(self, spawn_position,move_range):
        self.position = np.array([spawn_position[0],spawn_position[1],spawn_position[0] + 50, spawn_position[1] + 38])
        self.move_direction = 0
        self.count = 0
        self.move_range = np.array([move_range[0],move_range[1]])

    def move(self):
        self.position[0] += self.move_direction * 3
        self.position[2] += self.move_direction * 3

        self.count += 1
        if ((self.count % 10) == 0):
            self.move_direction = np.random.randint(-1,2)
            self.count = 0
        
    def bottomCheck(self):
        self.bottom_check = None
        collision = self.overlap_bottom(self.position, self.move_range)
        if not collision:
            if (self.position[0] < self.move_range[0]):
                self.position[0] = self.move_range[0]
                self.position[2] = self.position[0] + 30
            else :
                self.position[2] = self.move_range[1]
                self.position[0] = self.position[2] - 30


    def overlap_bottom(self, ego_position, other_position): #ego: 몬스터, otehr: 플랫폼
        return ego_position[0] > other_position[0] - 20 and ego_position[2] < other_position[1]

        
        """
        만약에 바닥 충돌일때만 : 이동
        5초마다 한번씩 방향을 바꿈 (rand -1, 1, 0)
        0이 아니면 state = move
        0이면 None?

        """