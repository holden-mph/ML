from process import get_data
import numpy as np

X, T = get_data()
N, D = X.shape

w = np.random.randn(D,1)

def sigmoid(a):
    return 1 / (1 + np.exp(-a))

Y = sigmoid(X.dot(w))

def cross_entropy(T, Y):
    E = 0
    for i in range(N):
        if T[i] == 1:
            E -= np.log(Y[i])
        else:
            E -= np.log(1-Y[i])
    return E
