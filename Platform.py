import numpy as np

class Platform:
    def __init__(self, pos):
        self.appearance = 'rectangle'
        self.position = np.array([pos[0], pos[1], pos[0] + pos[2], pos[1]+16])
        self.state = None

    def collision_check(self, character):
        collision = self.overlap(self.position, character.position)
        if collision:
            self.state = 'collision'

    def overlap(self, ego_position, other_position):     
        return ego_position[1] < other_position[3] and ego_position[3] > other_position[1] and ego_position[2] > other_position[2] - 20 and ego_position[0] < other_position[0] + 20