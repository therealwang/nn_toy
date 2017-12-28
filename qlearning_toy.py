# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:49:53 2017

@author: yuwan
"""

import numpy as np
from msvcrt import getch
import sys

class Game:
    def __init__(self, player, size, init = -1, goal = -1):
        self.player = player
        self.score = 0
        self.size = size
        if goal == -1:
            self.goal = self.size/2
        if init == -1:
            self.init = np.random.randint(1, self.size)
        self.player.position = self.init
        self.moves = 0
        
    def initboard(self):
        board = ['.'] * self.size
        board[0] = 'O'
        board[self.player.position] = '+'
        board[self.goal] = '#'
        return board
        
        
    def startgame(self):
        self.score = 0
        self.moves = 0
        self.displaygrid()
        while np.abs(self.score) < 3:
            move = self.player.move()
            if move == 'a':
                self.player.position -= 1
                self.moves += 1
            elif move == 'd' and self.player.position != self.size - 1:
                self.player.position += 1
                self.moves += 1
            if self.player.position == self.goal:
                self.score += 1
                self.player.position = self.init
            elif self.player.position == 0:
                self.score -= 1
                self.player.position = self.init
            self.displaygrid()
        print "\nScore: {0}, Moves: {1}".format(self.score, self.moves)
        
    def displaygrid(self):
        sys.stdout.flush()
        sys.stdout.write('\r' +  ''.join(self.initboard()) + '    Score: {0}'.format(self.score))

class Player:
    def __init__(self):
        self.position = 0
        
    def move(self):
        inp = ord(getch())
        if inp == 97:
            return 'a'
        elif inp == 100:
            return 'd'
        else:
            return
            
class qPlayer:
    #comment
    def __init__(self):
        self.position = 0