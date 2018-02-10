import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs

k = 4

X, y = make_blobs(n_samples=1000, n_features=k, centers=k)
plt.figure(figsize=(10,6))
plt.scatter(X[:,0], X[:,1])
plt.show()

centroid_coords_tracker = []

# Functions...
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

def label_clusters(distances):
    return np.array([distances[i].argmin(axis=0) for i in range(distances.shape[0])])
    
def reposition_centroids(data):
    for i in range(k):
        coords = []
        cluster = data[y==i]
        for j in range(cluster.shape[1]-1):
            coords.append(cluster[j].mean())
        centroid_coords[i] = tuple(coords)
    return centroid_coords

def plot_centroids():
    plt.figure(figsize=(10,6))
    plt.scatter(X[:,0], X[:,1])
    for i in range(k):
        plt.scatter(centroid_coords[i][0], centroid_coords[i][1], c='r', s=150)
    plt.show()
    
def converged(centroid_coords_tracker):
    if len(centroid_coords_tracker) >= 2:
        if centroid_coords_tracker[-1] == centroid_coords_tracker[-2]:
            return True
        else:
            return False
        
def get_clusters():    
    algorithm_converged = False
    
    while algorithm_converged == False:
        distances = calculate_distances()
        y = label_clusters(distances).reshape((X.shape[0],1))

        data = pd.DataFrame(np.concatenate((X,y),axis=1))
        centroid_coords = reposition_centroids(data)
        centroid_coords_tracker.append(centroid_coords)

        algorithm_converged = converged(centroid_coords_tracker)
        
    final_labels = label_clusters(calculate_distances()).reshape((X.shape[0],1))
    columns = ['feature_' + str(i+1) for i in range(X.shape[1]+1)]
    columns[-1] = 'cluster_label'
    
    return pd.DataFrame(np.concatenate((X,final_labels),axis=1),columns=columns)

def final_plot():
    plt.figure(figsize=(10,6))
    colours = ['g','b','r','y','c']
    results = [result[result['cluster_label']==i] for i in range(k)]
    for i in range(k):
        plt.scatter(results[i].iloc[:,0], results[i].iloc[:,1], c = colours[i])
    plt.show()
    
    
# Initialising centroids
centroid_coords = initialise_centroid_coords(X)
plot_centroids()

# Find clusters
result = get_clusters()
plot_centroids()
final_plot()
