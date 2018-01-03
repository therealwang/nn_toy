# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:49:53 2017

@author: yuwan
"""

import numpy as np
from msvcrt import getch
import sys

class Game:
    def __init__(self, size, init = -1, goal = -1):
        self.score = 0
        self.size = size
        if goal == -1:
            self.goal = self.size/2
        if init == -1:
            self.init = np.random.randint(1, self.size)
        
        self.moves = 0
    
    def addplayer(self, player):
        self.player = player
        self.player.position = self.init
        
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
            if move == 'a' and self.player.position != 0:
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
    def __init__(self, game, epsilon = 0.9, alpha = 0.9, gamma = 0.1):
        self.position = 0
        self.game = game
        self.size = game.size
        self.qmatrix = np.random.randn(self.size,2)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        
    def move(self):
        rn = np.random.rand()
        if rn > self.epsilon:
            ans = ['a','d'][np.random.randint(0,2)]
        else:
            poschoice = self.qmatrix[self.position]
            ans = ['a','d'][poschoice[1] > poschoice[0]] 
        if ans == 'a':
            action = 0
            newpos = max(self.position-1,0)
        else:
            action = 1
            newpos = min(self.position + 1, self.size - 1)
        if newpos == self.game.goal:
            reward = 1
        elif newpos == 0:
            reward = -1
        else:
            reward = 0
        self.updateq(self.position, action, newpos, reward)
        return ans
    
    def updateq(self, position, action, newpos, reward):
        oldval = self.qmatrix[position][action]
        self.qmatrix[position][action] = oldval + self.alpha*(reward +
                    self.gamma * max(self.qmatrix[newpos]) - oldval)
        
        
def qTrain(num = 10):
    g = Game(12)
    p = qPlayer(g)
    g.addplayer(p)
    for i in range(num):
        g.startgame()
    return g, p
        
        