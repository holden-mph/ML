import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df = pd.read_csv('dataset_Facebook.csv', sep=';')
df.drop('Type', inplace=True, axis=1)
df.dropna(inplace=True)

X = df.iloc[:,:-1]
#X = df[['comment','Paid']]
#X = df['comment']
y = df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#ALWAYS need to add an x_0 column

class LinearRegression(object):
    
    model_theta = 0
    
    def __init__(self):
        pass
    
    def get_h(self, X, theta):
        
        h = []   
        
        for i in range(len(X[0])):
            h_start = 0
            for j in range(theta.shape[0]):
                h_start += np.transpose(theta)[0][j]*X[j][i]
            h.append(h_start)
            
        return np.concatenate(h, axis=0)
    
    def shapeX(self, X):
        
        if len(X.shape) <= 1:
            X = X.reshape((len(X),1))
            
        X_j = np.zeros((X.shape[0], X.shape[1]+1))
        X_j[:,0] = 1
        X_j[:,1:] = X
        
        return [X_j[:,i].reshape(len(X_j[:,i]),1) for i in range(X_j.shape[1])]
        
    
    def fit(self, X, y):
        try:
            X = X.as_matrix()
            y = y.as_matrix()
        except:
            pass
        
        X_j = self.shapeX(X)
    
        theta_j = np.array([random.uniform(0,.1) for i in range(len(X_j))])
        theta_j = theta_j.reshape((len(theta_j),1))
        
        h = self.get_h(X_j, theta_j)
        
        m = len(h)
        
        def get_cost(h, y):
            paran = 0
            for i in range(m):
                paran += (h[i] - y[i])**2
            return (1/(2*m))*paran
        
        alpha = 1e-11
    
        cost_delta = 100
        cost_lst = []
        counter = 0
        
        while counter < 10000:
        
            for i in range(len(theta_j)):
                sigma = 0
                for j in range(m):
                    sigma += (h[j] - y[j])*X_j[i][j][0]
                theta_j[i] -= (alpha/m)*sigma
                
            h = self.get_h(X_j, theta_j)
            cost_lst.append(get_cost(h, y))
            
            try:
                cost_delta = abs(cost_lst[-1] - cost_lst[-2])
            except:
                pass
            counter += 1
            print('iteration: ', counter)
            
        self.model_theta = theta_j
    
    def predict(self, X):
        X_j = self.shapeX(X)
        return self.get_h(X_j, self.model_theta)
    
#doesn't work when X only has 1 feature
