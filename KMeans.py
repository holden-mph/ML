class KMeans(object):
    def __init__(self, n_clusters):
        self.k = n_clusters
        self.centroid_coords_tracker = []
        
    def fit_predict(self, X):
        self.X = X
        
        def rand_int(X):
            return np.random.randint(0,len(X))
        
        def initialise_centroid_coords(X):
            centroid_coords = []
            for centroid in range(self.k):
                centroid_k = []
                for i in range(X.shape[1]):
                    centroid_k.append(X[rand_int(X),i])
                centroid_coords.append(tuple(centroid_k))
            return centroid_coords
        
        def calculate_distances():
            distances = np.zeros((X.shape[0],self.k))
            for i in range(distances.shape[1]):
                distances[:,i] = np.sqrt(np.sum((X - centroid_coords[i])**2,axis=1))
            return distances
        
        def label_clusters(distances):
            return np.array([distances[i].argmin(axis=0) for i in range(distances.shape[0])])
        
        def reposition_centroids(data):
            for i in range(self.k):
                coords = []
                cluster = data[y==i]
                for j in range(cluster.shape[1]-1):
                    coords.append(cluster[j].mean())
                centroid_coords[i] = tuple(coords)
            return centroid_coords
        
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
                self.centroid_coords_tracker.append(centroid_coords)

                algorithm_converged = converged(self.centroid_coords_tracker)

            final_labels = label_clusters(calculate_distances()).reshape((X.shape[0],1))
            columns = ['feature_' + str(i+1) for i in range(X.shape[1]+1)]
            columns[-1] = 'cluster_label'

            return pd.DataFrame(np.concatenate((X,final_labels),axis=1),columns=columns)
        
        centroid_coords = initialise_centroid_coords(X)
        return get_clusters()
