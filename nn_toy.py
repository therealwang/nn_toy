# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:25:50 2017

@author: pressure102b
"""

import numpy as np


'''
Functions
'''
def dQuadCost(output, observation):
    return np.subtract(output,observation)

def dCrossEntropy(output, observation):
    return np.divide(np.subtract(output, observation),output * (1-output))
            
            
def Sigmoid(x):
    return 1/(1+np.exp(-1 * x))
    
def dSigmoid(x):
    return Sigmoid(x) * (1-Sigmoid(x))

'''
Network
'''

class Network:
    def __init__(self, layers, cost = dQuadCost):
        self.weights = [np.random.randn(i,j) for i,j in zip(layers[1:],layers)]
        self.biases = [np.random.randn(y,1) for y in layers[1:]]
        self.lenlayers = len(layers)
        self.costf = cost
        
    def SGD(self, train, epochs, batch, eta, test = None, lmb = 0):
        if test: n_test = len(test)
        self.n = len(train)
        for i in range(epochs):
            np.random.shuffle(train)
            batches = [train[k:k+batch] for k in range(0,self.n, batch)]
            for b in batches:
                self.train(b, eta, lmb)
            if test:
                print "Epoch {0}: {1} / {2}".format(
                        i, self.evaluate(test), n_test)
            else:
                print "Epoch {0} complete".format(i)
                
    
    def feedforward(self, input):
        temp = input
        for w, b in zip(self.weights, self.biases):
            temp = np.matmul(w,temp)+ b
            temp = Sigmoid(temp)
        return temp
        
    def classify(self, output):
        if output.size == 1:
            return (output > 0.5).astype(int)
        else:
            return (output == max(output)).astype(int)
         
    def evaluate(self, test):
        out = 0
        for data in test:
            input, observation = data
            output = self.classify(self.feedforward(input))
            if np.array_equal(output, observation):
                out += 1
        return out
        
        
            
    def train(self, batch, eta, lmb):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        
        for data in batch:
            input, observation = data
            errors = []
            forwardinputs = []
            forwardoutputs = [input]
    
            #feedforward
            temp = input
            for w,b in zip(self.weights, self.biases):
                temp = np.matmul(w, temp) + b
                forwardinputs.append(temp)
                temp = Sigmoid(temp)
                forwardoutputs.append(temp)
            
            #backprop
            output = forwardoutputs[-1]
            temperror = np.multiply(self.costf(output,observation), dSigmoid(forwardinputs[-1]))
            errors.append(temperror)
            for i in range(self.lenlayers-1)[::-1][:-1]:
                temperror = np.multiply(np.matmul(self.weights[i].transpose(),temperror),dSigmoid((forwardinputs[i-1])))
                errors.append(temperror)
            errors = list(reversed(errors))
        
            #adding errors
            nabla_b = [nb + err for nb, err in zip(nabla_b, errors)]
            nabla_w = [nw + err * fo.T for nw, err, fo in zip(nabla_w, errors, forwardoutputs)]
        '''
        inputs, obs = np.array([data[0] for data in batch]),np.array([data[1] for data in batch])
        errors = []
        forwardinputs = []
        forwardoutputs = [inputs]
        
        temp = inputs
        for w,b in zip(self.weights, self.biases):

            temp = np.matmul(w, temp) + b
            forwardinputs.append(temp)
            temp = Sigmoid(temp)
            forwardoutputs.append(temp)
 
        
        #backprop
        output = forwardoutputs[-1]
        temperror = np.multiply(self.costf(output,obs), dSigmoid(forwardinputs[-1]))
        errors.append(temperror)
        for i in range(self.lenlayers-1)[::-1][:-1]:
            temperror = np.multiply(np.matmul(self.weights[i].T,temperror),dSigmoid((forwardinputs[i-1])))
            errors.append(temperror)
        errors = list(reversed(errors))
        
    
        
        nabla_b = [sum(error) for error in errors]
        nabla_w = [sum(np.matmul(err, fo.transpose(0,2,1))) for err, fo in zip(errors, forwardoutputs)]
    
       
        '''
        self.weights = [w * (1 - eta * lmb/self.n) - nw*(eta/len(batch)) for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - nb*(eta/len(batch)) for b, nb in zip(self.biases, nabla_b)]

