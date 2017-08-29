import numpy as np
from collections import Counter

class KNN(object):
    
    def __init__(self, k=3):
        self.k = k
        
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        predictions = np.zeros((X_test.shape[0], 1))
        
        for test_idx, test_row in enumerate(X_test):
            arr = np.zeros((self.X_train.shape[0], 2))
            
            for train_idx, train_row in enumerate(self.X_train):
                diff = train_row - test_row
                arr[train_idx, 0] = np.sqrt(diff.dot(diff))
                arr[train_idx, 1] = train_idx
                
            k_nearest = arr[arr[:,0].argsort()][0:self.k,1]
            y_votes = [self.y_train[int(i)] for i in k_nearest]
            row_pred = Counter.most_common(Counter(y_votes))[0][0]
            predictions[test_idx, 0] = row_pred
            
        return predictions
