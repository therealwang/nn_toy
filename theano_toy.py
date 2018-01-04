# -*- coding: utf-8 -*-
"""
Created on Wed Jan 03 19:18:59 2018

@author: yuwan
"""

import theano
import theano.tensor as T
from theano import In, shared

a = T.vector()
b = T.vector()
out = a**2 + b**2 + 2*a*b
diff = a-b
absdiff = abs(a-b)

f = theano.function([a,b],[out,diff,absdiff])
print f([0,1,2],[1,2,3])

x = T.dmatrix('x')
s = 1/(1+T.exp(-x))
logistic = theano.function([x],s)
print logistic([[0,1,],[-1,-2]])

inc = T.iscalar()
state = shared(0)
accumulator = theano.function([inc], state, updates= [(state,state+inc)])

print state.get_value()
accumulator(3)
print state.get_value()

newstate = shared(0)
newaccumulator = accumulator.copy(swap={state:newstate})

print newstate.get_value()
newaccumulator(3)
print newstate.get_value()