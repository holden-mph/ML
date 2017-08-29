import numpy as np

N = 100
D = 1

X = np.random.rand(N,D)
y = 0.5*X + 0.8 + np.random.rand(N,D)*0.1

N, D = X.shape
w = np.random.rand(1,D+1)
X = np.concatenate((np.ones((N,1)),X),axis=1)
h = X.dot(w.T)

def cost(h, y):
    return (1/(2*N)) * np.sum((h - y)**2)

cost = cost(h, y)

alpha = 0.01
epochs = 10000

for i in range(epochs):
    w -
