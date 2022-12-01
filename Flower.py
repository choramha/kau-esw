import numpy as np

class Flower:
    def __init__(self,position):
        self.position = np.array([position[0],position[1],position[0] + 40,position[1] - 40])
        self.state = None

        
    def collision_check(self, character):
        self.state = None
        #print("position CHeck: ",self.position, character.position)
        collision = self.overlap(self.position, character.position)
        #print(collision)

        if collision:
            self.state = 'get'

    def overlap(self, ego_position, other_position):
        #print("overlapCheck",ego_position,other_position)
        return ego_position[0] < other_position[2] and ego_position[2] > other_position[0] and ego_position[1] + 20 > other_position[3] and ego_position[3] < other_position[1]

