import numpy as np
import random

def distance_to_danger(x,y,a_f,b_f):

    proj_x = (-b_f + y + a_f * x) / 2 / a_f
    proj_y = a_f * proj_x + b_f
    
    return (x - proj_x)**2 + (y - proj_y)**2

class Problem:
    
    def __init__(self, w_h, w_l, w_f, a_f, b_f, x_e):
        
        self.w_h = w_h
        self.w_l = w_l
        self.w_f = w_f
        self.a_f = a_f
        self.b_f = b_f
        self.x_e = x_e
        self.n = None
        self.W = None
        self.X_b = None
        self.Y_b = None
        self.c = None
        self.step = None
        self.agent_list = None
        self.lims = None
        self.d_e = 0.1

    def true_objective(self, X):
        
        total = 0

        # first n entries are X, last n entries are Y
        for i in range(self.n):
            if self.agent_list[i] == 'follower':
                total += self.w_f / 2 * (X[i] - self.X_b[i])**2
                total += self.w_f / 2 * (X[i+self.n] - self.Y_b[i])**2
            elif self.agent_list[i] == 'helper':
                total += - self.w_h * np.log(self.b_f - X[i+self.n] - self.a_f * X[i])
            elif self.agent_list[i] == 'leader':
                total += self.w_l / 2 * (X[i] - self.x_e - self.d_e)**2
                
        return total
    
    def objective(self, X):
        
        I = np.identity(self.n)
        XX = X[:self.n]
        YY = X[self.n:]
        
        consensus = np.linalg.norm((I-self.W) @ XX)**2 + np.linalg.norm((I-self.W) @ YY)**2
        
        return 1 / 2 / self.step * consensus + self.true_objective(X)
    
    def true_gradient(self, X):
        
        out = np.zeros_like(X)
        
        # first n entries are X, last n entries are Y
        for i in range(self.n):
            if self.agent_list[i] == 'follower':
                out[i] = self.w_f * (X[i] - self.X_b[i])
                out[i+self.n] = self.w_f * (X[i+self.n] - self.Y_b[i])
            elif self.agent_list[i] == 'helper':
                out[i] = - self.w_h * self.a_f / (self.b_f - X[i+self.n] - self.a_f * X[i])
                out[i+self.n] = - self.w_h / (self.b_f - X[i+self.n] - self.a_f * X[i])
            else:
                out[i] = self.w_l / 2 * (X[i] - self.x_e - self.d_e)
        
        return out

def initialize(n,a_f,b_f,x_e, n_leaders, n_helpers):

    n_followers = n -n_leaders -n_helpers # number of followers 
    agent_list = ['follower'] * n # initialize list as followers

    # Pick random X values in [0,x_e]
    X_0 = np.random.rand(n) * x_e
    
    # Generate feasible Y values
    Y_0 = np.zeros(n)
    
    for i in range(n):
        
        if b_f > 1 and X_0[i] < (1 - b_f) / a_f:
            upper_bound = 1
        else:
            upper_bound = a_f * X_0[i] + b_f
     
        Y_0[i] = np.random.rand() * upper_bound

    # find the agents closest to danger and assign them helper role
    dists_to_danger = np.array([distance_to_danger(X_0[i], Y_0[i], a_f, b_f) for i in range(n)])
    dist_indices = np.argsort(dists_to_danger)
    helper_indices = dist_indices[:n_helpers]
    leader_indices = random.sample(list(dist_indices[n_helpers:]), n_leaders)

    for index in helper_indices:
        agent_list[index] = 'helper'
    for index in leader_indices:
        agent_list[index] = 'leader'
    
    return X_0, Y_0, agent_list

    