import numpy as np

class Enemy:
    def __init__(self, spawn_position):
        self.appearance = 'circle'
        self.state = 'alive'
        self.position = np.array([spawn_position[0], spawn_position[1], spawn_position[0] + 40, spawn_position[1] - 40])
        self.outline = "#00FF00"

    
        