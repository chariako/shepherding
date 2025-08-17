import networkx as nx
import numpy as np

def metropolis(L):
    
    D = np.sum(L,1)
    n = len(D)
    
    W = np.zeros_like(L, dtype=float)
    
    for i in range(n):
        for j in range(i,n):
            if L[i,j]:
                
                W[i,j] = W[j,i] = 1 / (1 + max(D[i],D[j]))
        
    for i in range(n):
        W[i,i] = 1 - np.sum(W[i,:])
        
    return W

def dist(x1, y1, x2, y2):

    return (x1-x2)**2 + (y1 - y2)**2

def generate_W(X_0,Y_0):
    
    n = len(X_0)
    Dist = np.zeros((n, n))  # distances between agents

    for i in range(n):
        for j in range(i+1, n):

            dd = dist(X_0[i], Y_0[i], X_0[j], Y_0[j])
            Dist[i, j] = dd
            Dist[j, i] = dd

    R = .01
    A = (Dist < R).astype(int)
    np.fill_diagonal(A, 0)
    G = nx.from_numpy_array(A)

    while not nx.is_connected(G):

        R = R + 0.01
        A = (Dist < R).astype(int)
        np.fill_diagonal(A, 0)
        G = nx.from_numpy_array(A)

    W = metropolis(A)
    
    return W