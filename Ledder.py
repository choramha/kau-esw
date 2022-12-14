import numpy as np

class Ledder:
    def __init__(self, position):
        self.appearance = 'rectangle'
        self.position = np.array([position[0], position[1], position[0] + 32, position[1] + 154])
        self.state = None

    def collision_check(self, character):
        collision = self.overlap(self.position, character.position)

        if collision:
            self.state = 'collision'

    def overlap(self, ego_position, other_position):
        return ego_position[0] - 10 < other_position[0] and ego_position[2] + 20 > other_position[2] and (ego_position[1] - 40) < other_position[1]