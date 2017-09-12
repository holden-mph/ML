import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=100, n_features=2, centers=3, random_state=3)
plt.scatter(X[:,0], X[:,1],c=y)
plt.show()

k = 3

def rand_int(X):
    return np.random.randint(0,len(X))

def initialise_centroid_coords(X):
    centroid_coords = []
    for centroid in range(k):
        centroid_k = []
        for i in range(X.shape[1]):
            centroid_k.append(X[rand_int(X),i])
        centroid_coords.append(tuple(centroid_k))
    return centroid_coords

def calculate_distances():
    distances = np.zeros((X.shape[0],k))
    for i in range(distances.shape[1]):
        distances[:,i] = np.sqrt(np.sum((X - centroid_coords[i])**2,axis=1))
        
    return distances

def label_clusters():
    return np.array([distances[i].argmin(axis=0) for i in range(distances.shape[0])])
    
def reposition_centroids():
    for i in range(k):
        coords = []
        cluster = data[y==i]
        for j in range(cluster.shape[1]-1):
            coords.append(cluster[j].mean())
        centroid_coords[i] = tuple(coords)
    return centroid_coords
    
centroid_coords = initialise_centroid_coords(X)

plt.scatter(X[:,0], X[:,1])
plt.scatter(centroid_coords[0][0], centroid_coords[0][1], c='r')
plt.scatter(centroid_coords[1][0], centroid_coords[1][1], c='r')
plt.scatter(centroid_coords[2][0], centroid_coords[2][1], c='r')
plt.show()

distances = calculate_distances()
y = label_clusters().reshape((X.shape[0],1))

data = pd.DataFrame(np.concatenate((X,y),axis=1))
centroid_coords = reposition_centroids()

plt.scatter(X[:,0], X[:,1])
plt.scatter(centroid_coords[0][0], centroid_coords[0][1], c='r')
plt.scatter(centroid_coords[1][0], centroid_coords[1][1], c='r')
plt.scatter(centroid_coords[2][0], centroid_coords[2][1], c='r')
plt.show()
