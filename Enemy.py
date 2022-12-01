import numpy as np

class Enemy_gasi:
    def __init__(self, position):
        self.position = np.array([position[0],position[1],position[0]+34,position[1]+18])

