# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:49:53 2017

@author: yuwan
"""

import numpy as np

class Game:
    def __init__(self, size, init = -1, goal = -1):
        self.iter = 0
        self.size = size
        if init == -1:
            self.init = np.randint(1, self.size)
        if goal == -1:
            self.goal = self.size/2

class Player:
    def __init__(self):
        self.score = 0
        
    def move(self, inp):
        if inp == 'a':
            return 'a'
        elif inp == 'd':
            return 'd'
        else:
            return
            
class qPlayer:
    #comment