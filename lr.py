import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split

df = pd.read_csv('dataset_Facebook.csv', sep=';')
df.drop('Type', inplace=True, axis=1)
df.dropna(inplace=True)

X = df.iloc[:,:-1]
y = df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#ALWAYS need to add an x_0 column

class LinearRegression(object):
    
    def __init__(self):
        pass
    
    def fit(self, x, y):
        pass
    
    def predict(self, x, y):
        pass
    
#user will say: model = LinearRegression(), model.fit(X_train, y_train)
    
#need h, randomly intialise theta, gradient descent equation, column of x_0 = 1

X = X_train.as_matrix() #x = x.as_matrix()
y = y_train.as_matrix()

if len(X.shape) <= 1:
    X = X.reshape((len(X),1))

X_j = np.zeros((X.shape[0], X.shape[1]+1))
X_j[:,0] = 1
X_j[:,1:] = X
X_j = [X_j[:,i].reshape(len(X_j[:,i]),1) for i in range(X_j.shape[1])]

theta_j = np.array([random.uniform(0,.1) for i in range(len(X_j))])
theta_j = theta_j.reshape((len(theta_j),1))

def get_h(X_j, theta_j):
    h = []   
    for i in range(len(X_j[0])):
        h_start = 0
        for j in range(theta_j.shape[0]):
            h_start += np.transpose(theta_j)[0][j]*X_j[j][i]
        h.append(h_start)
    return np.concatenate(h, axis=0)

h = get_h(X_j, theta_j)


# use this initial h to calculate the squared error

m = len(h)

def get_cost(h, y):
    paran = 0
    for i in range(m):
        paran += (h[i] - y[i])**2
    return (1/(2*m))*paran

cost = get_cost(h, y)
alpha = 1e-11

#Gradient Descent

cost_delta = 1
cost_lst = []
counter = 0

while cost_delta > 0.09:

    for i in range(len(theta_j)):
        sigma = 0
        for j in range(m):
            sigma += (h[j] - y[j])*X_j[i][j][0]
        theta_j[i] -= (alpha/m)*sigma
        
    h = get_h(X_j, theta_j)
    cost_lst.append(get_cost(h, y))
    
    try:
        cost_delta = abs(cost_lst[-1] - cost_lst[-2])
    except:
        pass
    counter += 1
    print('iteration: ', counter)

import matplotlib.pyplot as plt


#think about how all this fits into .fit and .predict methods
