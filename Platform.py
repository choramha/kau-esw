import numpy as np

class Platform:
    def __init__(self, pos):
        self.position = np.array([pos[0], pos[1], pos[0] + pos[2], pos[1]+pos[3]]) #(x축, y축, 넓이, 높이)
        self.state = None

class Goal:
    def __init__(self, pos):
        self.position = np.array([pos[0],pos[1],pos[0] + 30, pos[1] + 30])
        self.state = None

    def collision_check(self, character):
        collision = self.overlap(self.position, character.position)

        if collision:
            self.state = 'clear'

    def overlap(self, ego_position, other_position):
        return ego_position[2] > other_position[0] and ego_position[3] > other_position[1] \
        and ego_position[0] < other_position[2] and ego_position[3] < other_position[3] + 5