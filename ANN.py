import numpy as np
import pandas as pd
import tensorflow as tf

import matplotlib.pyplot as plt
%matplotlib inline

Nclass = 500

X1 = np.random.randn(Nclass,2) + np.array([-2,2])
X2 = np.random.randn(Nclass,2) + np.array([-6,6])
X3 = np.random.randn(Nclass,2) + np.array([4,6])
X = pd.DataFrame(np.vstack([X1,X2,X3]))
Y = pd.DataFrame(np.array([0]*Nclass + [1]*Nclass + [2]*Nclass))

df = pd.concat([X, Y], axis=1)
df = df.sample(frac=1)

X = df.iloc[:,:-1].as_matrix()
Y = df.iloc[:,-1].as_matrix()

### Defining the neural network architecture ### MULTI CLASS
N, D = X.shape
K = len(set(Y))

N_batches = 15
batch_size = int(X.shape[0] / N_batches)

alpha = 0.001
epochs = 1000

def indicator_matrix(Y, N, K):
    T = np.zeros((N,K))
    for i in range(N):
        T[i, Y[i]] = 1
    return T

def get_batch(idx):
    return X[idx*batch_size : (idx+1)*batch_size, :], Y[idx*batch_size : (idx+1)*batch_size]

T = indicator_matrix(Y, N, K)

N_hidden_layers = 3
N_nodes = [8,8,8]

assert(N_hidden_layers == len(N_nodes))

hidden_layer_nodes = {('M' + str(i+1)) : N_nodes[i] for i in range(len(N_nodes))}
weight_dims = {('W' + str(i+1)) : None for i in range(len(N_nodes)+1)}
weights = {('W' + str(i+1)) : None for i in range(len(N_nodes)+1)}
biases = {('B'+str(i+1)) : None for i in range(N_hidden_layers + 1)}

Z = {('Z')+str(i+1) : None for i in range(N_hidden_layers + 1)}

# FIT
### Initialising the weights ###

def get_weight_dims(D,K):
    weight_dims['W1'] = (D,hidden_layer_nodes['M1'])

    for i in range(1,len(weight_dims)):
        if i != len(weight_dims) - 1:
            weight_dims['W'+str(i+1)] = (hidden_layer_nodes['M'+str(i)],hidden_layer_nodes['M'+str(i+1)])
        else:
            weight_dims['W'+str(i+1)] = (hidden_layer_nodes['M'+str(i)], K)
    
    return weight_dims

def init_weights(weight_dims):
    
    for i in range(len(weights)):
        weights['W'+str(i+1)] = tf.Variable(tf.random_normal(weight_dims['W'+str(i+1)],dtype=tf.float64),dtype=tf.float64)
    
    return weights

weight_dims = get_weight_dims(D,K)
weights = init_weights(weight_dims)

### Initialising the biases ###

def init_biases():

    for i in range(len(biases)):
        b = np.random.randn(weight_dims['W'+str(i+1)][1])
        biases['B'+str(i+1)] = tf.Variable(b, dtype=tf.float64)

    return biases

biases = init_biases()

### Forward propagation ###

def forward(X, weights, biases):
    
    Z['Z1'] = tf.nn.tanh(tf.add(tf.matmul(X, weights['W1']),biases['B1']))
    
    for i in range(2,len(Z)):
        Z['Z'+str(i)] = tf.add(tf.matmul(Z['Z'+str(i-1)], weights['W'+str(i)]), biases['B'+str(i)])
        Z['Z'+str(i)] = tf.nn.tanh(Z['Z'+str(i)])                    
        
    Z['Z'+str(len(Z))] = tf.add(tf.matmul(Z['Z'+str(len(Z)-1)], weights['W'+str(len(weights))]), 
                                       biases['B'+str(len(biases))])
                               
    return Z['Z'+str(len(Z))]

tfX = tf.placeholder(dtype=tf.float64, shape=[None, D])
tfY = tf.placeholder(dtype=tf.float64, shape=[None, K])
   
p_y_given_x = forward(X, weights, biases)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=T, logits=p_y_given_x))
optimiser = tf.train.GradientDescentOptimizer(learning_rate=alpha).minimize(cost)
predict = tf.argmax(p_y_given_x, 1)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    
    sess.run(init)
    
    for i in range(epochs):
        
        for b in range(N_batches):
            X_batch, Y_batch = get_batch(b)
            N_batch = X_batch.shape[0]
            T_batch = indicator_matrix(Y_batch, N_batch, K)
            sess.run(optimiser, feed_dict={tfX : X_batch, tfY : T_batch})
            pred = sess.run(predict, feed_dict={tfX : X_batch, tfY : T_batch})
        
        print('Epoch',i+1,'complete')
        print('Accuracy:',np.mean(Y==pred))
