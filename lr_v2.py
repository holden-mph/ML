import numpy as np
import matplotlib.pyplot as plt

N = 10
D = 3
X = np.zeros((N, D))
X[:,0] = 1 # bias term
X[:5,1] = 1
X[5:,2] = 1
Y = np.array([0]*5 + [1]*5)

N, D = X.shape
w = np.random.rand(D+1)
X = np.concatenate((np.ones((N,1)),X),axis=1)
h = X.dot(w.T)

def cost(h, y):
    return (1/(2*N)) * np.sum((h - y)**2)

alpha = 0.01
cost_list = []

for i in range(10000):
    w -= alpha * X.T.dot(h-y)
    h = X.dot(w.T)
    if i % 100 == 0:
        print(cost(h,y))

#converged = False
#while converged == False:
#    w -= alpha * (h-y).T.dot(X)
#    h = X.dot(w.T)
#    cost_list.append(cost(h,y))
#    if len(cost_list) % 50 == 0:
#        if (cost_list[-1] / cost_list[-2] - 1) < 0.001:
#            converged = True
