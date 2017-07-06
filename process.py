import numpy as np
import pandas as pd

def get_data():
    df = pd.read_excel('ecom.xlsx')
    df = df[df['user_action'] < 2].as_matrix()
    
    X = df[:,:-1]
    Y = df[:,-1]
    
    N, D = X.shape
    Y = Y.reshape(N,1)
    
    X[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()
    X[:,2] = (X[:,2] - X[:,2].mean()) / X[:,2].std()
    
    X2 = np.concatenate((np.ones((N,1)), np.zeros((N, D+2))), axis=1)
    X2[:,1:5] = X[:,0:4] 
    X2[:,5:] = pd.get_dummies(X[:,-1], drop_first=True)
    return X2, Y

